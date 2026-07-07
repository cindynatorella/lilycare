from __future__ import annotations

import calendar
from datetime import date, datetime
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, session, url_for

from .demo_data import build_default_state

from backend.db import configure_database, db

from backend import pet_repository
from backend import vet_repository

from backend.models import PetProfile
from backend.models import VetLink

import os

# Build the Flask app, register routes, and connect the UI to session data.
def create_app() -> Flask:
	app = Flask(__name__)
	app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")

	configure_database(app) #Connect to the db

	# Render the main dashboard with Lily's profile, vaccines, and vet links.
	@app.route("/")
	def dashboard():
		state = _load_state()
		today = date.today()

		pet_profile = pet_repository.get_pet_profile()

		if pet_profile is None:
			profile = state["profile"]
		else:
			profile = pet_profile.to_dict()


		vaccines = [_decorate_vaccine(vaccine, today) for vaccine in state["vaccines"]]
		vaccines.sort(key=_vaccine_sort_key)

		counts = {
			"current": sum(1 for vaccine in vaccines if vaccine["status_key"] == "current"),
			"due_soon": sum(1 for vaccine in vaccines if vaccine["status_key"] == "due_soon"),
			"overdue": sum(1 for vaccine in vaccines if vaccine["status_key"] == "overdue"),
		}

		next_due = next((vaccine for vaccine in vaccines if vaccine["next_due_date"]), None)

		# Vet links
		try:
			vet_links = vet_repository.list_vet_links()

			if vet_links:
				vets = [vet_link.to_dict() for vet_link in vet_links]
			else:
				vets = []
		except Exception:
			vets = []

		#rendering
		return render_template(
			"dashboard.html",
			profile=_decorate_profile(profile, today),
			vaccines=vaccines,
			vets=vets,
			total_vaccines=len(vaccines),
			today_label=_format_date(today),
			next_due=next_due,
			counts=counts,
		)

	# Save profile edits made from the Lily section of the dashboard.
	@app.post("/profile")
	def update_profile():
		state = _load_state()

		birth_date_text = request.form.get("birth_date", "").strip()
		description = request.form.get("description", "").strip()

		pet_profile = pet_repository.get_pet_profile()

		if pet_profile is None:
			state["profile"]["birth_date"] = birth_date_text
			state["profile"]["description"] = description
			_save_state(state)
		else:
			updated_profile = PetProfile(
				name=pet_profile.name,
				birth_date=_safe_parse_date(birth_date_text),
				description=description,
			)

			pet_repository.update_pet_profile(updated_profile)

		flash("Lily's profile has been updated.", "success")
		return redirect(url_for("dashboard", _anchor="profile"))

	# Create a new vaccine reminder card from the add form.
	@app.post("/vaccines")
	def add_vaccine():
		state = _load_state()
		name = request.form.get("name", "").strip()
		description = request.form.get("description", "").strip()
		note = request.form.get("note", "").strip()
		recurrence_months = request.form.get("recurrence_months", "").strip()
		next_due = request.form.get("next_due", "").strip()
		history_text = request.form.get("history", "").strip()

		if not name or not recurrence_months or not next_due:
			flash("Add a vaccine name, recurrence, and next due date to create a card.", "error")
			return redirect(url_for("dashboard", _anchor="vaccines"))

		try:
			recurrence_value = int(recurrence_months)
			if recurrence_value <= 0:
				raise ValueError
			_parse_date(next_due)
			history = _parse_history(history_text)
		except ValueError:
			flash("Use a positive month interval and valid vaccine dates.", "error")
			return redirect(url_for("dashboard", _anchor="vaccines"))

		state["vaccines"].append(
			{
				"id": uuid4().hex[:8],
				"name": name,
				"description": description or "Custom vaccine reminder.",
				"note": note,
				"recurrence_months": recurrence_value,
				"next_due": next_due,
				"last_given": history[0] if history else "",
				"history": history,
			}
		)
		_save_state(state)
		flash(f"{name} was added to Lily's vaccine tracker.", "success")
		return redirect(url_for("dashboard", _anchor="vaccines"))

	# Mark a vaccine as completed today and roll the due date forward.
	@app.post("/vaccines/<vaccine_id>/complete")
	def complete_vaccine(vaccine_id: str):
		state = _load_state()

		for vaccine in state["vaccines"]:
			if vaccine["id"] != vaccine_id:
				continue

			recurrence_months = int(vaccine.get("recurrence_months", 0) or 0)
			if recurrence_months <= 0:
				flash("That vaccine needs a recurrence interval before it can roll forward.", "error")
				return redirect(url_for("dashboard", _anchor="vaccines"))

			today = date.today()
			vaccine["last_given"] = today.isoformat()
			vaccine["next_due"] = _add_months(today, recurrence_months).isoformat()
			history = _normalize_history(vaccine.get("history", []))
			today_value = today.isoformat()
			if today_value not in history:
				history.insert(0, today_value)
			vaccine["history"] = history
			_save_state(state)
			flash(f"{vaccine['name']} was marked complete and rolled to the next due date.", "success")
			return redirect(url_for("dashboard", _anchor="vaccines"))

		flash("That vaccine card could not be found in the current session.", "error")
		return redirect(url_for("dashboard", _anchor="vaccines"))

	# Save changes to an existing vaccine, including notes and history.
	@app.post("/vaccines/<vaccine_id>/update")
	def update_vaccine(vaccine_id: str):
		state = _load_state()

		for vaccine in state["vaccines"]:
			if vaccine["id"] != vaccine_id:
				continue

			name = request.form.get("name", "").strip()
			description = request.form.get("description", "").strip()
			note = request.form.get("note", "").strip()
			recurrence_months = request.form.get("recurrence_months", "").strip()
			next_due = request.form.get("next_due", "").strip()
			history_text = request.form.get("history", "").strip()

			if not name or not recurrence_months or not next_due:
				flash("Vaccine name, recurrence, and due date are required.", "error")
				return redirect(url_for("dashboard", _anchor="vaccines"))

			try:
				recurrence_value = int(recurrence_months)
				if recurrence_value <= 0:
					raise ValueError
				_parse_date(next_due)
				history = _parse_history(history_text)
			except ValueError:
				flash("Use valid dates and a positive recurrence interval.", "error")
				return redirect(url_for("dashboard", _anchor="vaccines"))

			vaccine["name"] = name
			vaccine["description"] = description or "Custom vaccine reminder."
			vaccine["note"] = note
			vaccine["recurrence_months"] = recurrence_value
			vaccine["next_due"] = next_due
			vaccine["history"] = history
			vaccine["last_given"] = history[0] if history else ""
			_save_state(state)
			flash(f"{name} was updated.", "success")
			return redirect(url_for("dashboard", _anchor="vaccines"))

		flash("That vaccine card could not be found in the current session.", "error")
		return redirect(url_for("dashboard", _anchor="vaccines"))

	# Remove a vaccine card from the current session.
	@app.post("/vaccines/<vaccine_id>/delete")
	def delete_vaccine(vaccine_id: str):
		state = _load_state()
		original_count = len(state["vaccines"])
		state["vaccines"] = [
			vaccine for vaccine in state["vaccines"] if vaccine["id"] != vaccine_id
		]

		if len(state["vaccines"]) == original_count:
			flash("That vaccine card could not be found in the current session.", "error")
			return redirect(url_for("dashboard", _anchor="vaccines"))

		_save_state(state)
		flash("The vaccine card was deleted.", "success")
		return redirect(url_for("dashboard", _anchor="vaccines"))

	# Add a new vet link that Lily's dashboard can open quickly.
	@app.post("/vets")
	def add_vet():
		name = request.form.get("name", "").strip()
		url = request.form.get("url", "").strip()
		notes = request.form.get("notes", "").strip()

		if not name or not url:
			flash("Add both a vet name and a booking link.", "error")
			return redirect(url_for("dashboard", _anchor="vets"))

		if not url.startswith(("http://", "https://")):
			url = f"https://{url}"

		vet_link = VetLink(
			name=name,
			url=url,
			notes=notes or "Booking link saved for future appointments.",
		)

		try:
			vet_repository.create_vet_link(vet_link)
			flash(f"{name} was added to Lily's vet links.", "success")

		except Exception as error:
			print("Could not save vet link to database:", error)
			db.session.rollback()
			flash("The vet link could not be saved because the database had an error.", "error")

		return redirect(url_for("dashboard", _anchor="vets"))

	# Save edits to an existing vet link card.
	@app.post("/vets/<int:vet_id>/update")
	def update_vet(vet_id: int):
		name = request.form.get("name", "").strip()
		url = request.form.get("url", "").strip()
		notes = request.form.get("notes", "").strip()

		if not name or not url:
			flash("Vet name and booking URL are required.", "error")
			return redirect(url_for("dashboard", _anchor="vets"))

		if not url.startswith(("http://", "https://")):
			url = f"https://{url}"

		updated_vet = VetLink(
			id=vet_id,
			name=name,
			url=url,
			notes=notes or "Booking link saved for future appointments.",
		)

		try:
			saved_vet = vet_repository.update_vet_link(updated_vet)

			if saved_vet is None:
				flash("That vet link could not be found.", "error")
			else:
				flash(f"{name} was updated.", "success")

		except Exception as error:
			print("Could not update vet link in database:", error)
			db.session.rollback()
			flash("The vet link could not be updated because the database had an error.", "error")

		return redirect(url_for("dashboard", _anchor="vets"))


	# Remove a vet link card from PostgreSQL.
	@app.post("/vets/<int:vet_id>/delete")
	def delete_vet(vet_id: int):
		try:
			deleted = vet_repository.delete_vet_link(vet_id)

			if deleted:
				flash("The vet link was deleted.", "success")
			else:
				flash("That vet link could not be found.", "error")

		except Exception as error:
			print("Could not delete vet link from database:", error)
			db.session.rollback()
			flash("The vet link could not be deleted because the database had an error.", "error")

		return redirect(url_for("dashboard", _anchor="vets"))

	# Reset the session back to the original demo data.
	@app.post("/reset-demo")
	def reset_demo():
		session["lilycare_state"] = build_default_state()
		session.modified = True
		flash("The dashboard was reset back to the starter LilyCare demo data.", "success")
		return redirect(url_for("dashboard"))

	return app


# Read the current in-session app state, creating it on first load.
def _load_state() -> dict:
	state = session.get("lilycare_state")
	if state is None:
		state = build_default_state()
		session["lilycare_state"] = state
		session.modified = True
	return state


# Persist updated session data after a form submission.
def _save_state(state: dict) -> None:
	session["lilycare_state"] = state
	session.modified = True


# Convert a YYYY-MM-DD string into a Python date object.
def _parse_date(value: str) -> date:
	return datetime.strptime(value, "%Y-%m-%d").date()


# Format Python dates into the shorter labels shown in the UI.
def _format_date(value: date | None) -> str:
	if value is None:
		return "Not set"
	return value.strftime("%b %d, %Y")


# Turn a month interval into a friendlier recurrence label.
def _recurrence_label(months: int) -> str:
	if months <= 0:
		return "Custom schedule"
	if months == 1:
		return "Every month"
	if months == 12:
		return "Every year"
	return f"Every {months} months"


# Calculate Lily's age display from her birth date.
def _pet_age_label(birth_date: date | None, today: date) -> str:
	if birth_date is None:
		return "Add Lily's birthday"

	months_apart = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
	if today.day < birth_date.day:
		months_apart -= 1

	years, months = divmod(max(months_apart, 0), 12)

	if years and months:
		return f"{years} yr {months} mo"
	if years:
		return f"{years} years old"
	return f"{months} months old"


# Categorize a vaccine based on how close its due date is.
def _status_for_due_date(next_due: date | None, today: date) -> tuple[str, str, str]:
	if next_due is None:
		return "unknown", "Needs date", "Add a due date to track this vaccine."

	days_until = (next_due - today).days
	if days_until < 0:
		return "overdue", "Overdue", f"{abs(days_until)} day(s) overdue."
	if days_until == 0:
		return "due_soon", "Due today", "This vaccine is due today."
	if days_until <= 30:
		return "due_soon", "Due soon", f"Due in {days_until} day(s)."
	return "current", "Current", f"{days_until} day(s) until due."


# Prepare Lily's profile values for display in the template.
def _decorate_profile(profile: dict, today: date) -> dict:
	birth_date = _safe_parse_date(profile.get("birth_date", ""))
	description = profile.get("description", "").strip() or (
		"Add a short note about Lily's personality, care routine, or vaccine preferences."
	)
	return {
		**profile,
		"description": description,
		"birth_date_label": _format_date(birth_date),
		"age_label": _pet_age_label(birth_date, today),
	}


# Prepare each vaccine card with labels, status, and editable values.
def _decorate_vaccine(vaccine: dict, today: date) -> dict:
	next_due = _safe_parse_date(vaccine.get("next_due", ""))
	history = _normalize_history(vaccine.get("history", []))
	last_given = _safe_parse_date(history[0]) if history else _safe_parse_date(vaccine.get("last_given", ""))
	status_key, status_label, status_hint = _status_for_due_date(next_due, today)

	return {
		**vaccine,
		"next_due_date": next_due,
		"next_due_label": _format_date(next_due),
		"last_given_label": _format_date(last_given),
		"next_due_value": next_due.isoformat() if next_due else "",
		"note": vaccine.get("note", "").strip(),
		"history": history,
		"history_labels": [_format_date(_safe_parse_date(value)) for value in history],
		"history_text": "\n".join(history),
		"recurrence_label": _recurrence_label(int(vaccine.get("recurrence_months", 0) or 0)),
		"status_key": status_key,
		"status_label": status_label,
		"status_hint": status_hint,
	}


# Sort vaccines so the earliest due dates appear first.
def _vaccine_sort_key(vaccine: dict) -> tuple[int, date]:
	next_due = vaccine.get("next_due_date")
	if next_due is None:
		return (1, date.max)
	return (0, next_due)


# Try to parse a date, but return None instead of crashing on bad input.
def _safe_parse_date(value: str) -> date | None:
	if not value:
		return None
	try:
		return _parse_date(value)
	except ValueError:
		return None


# Clean a history list by removing blanks, bad dates, and duplicates.
def _normalize_history(values: list[str]) -> list[str]:
	normalized: list[str] = []
	seen = set()

	for value in values:
		parsed = _safe_parse_date(value)
		if parsed is None:
			continue
		iso_value = parsed.isoformat()
		if iso_value in seen:
			continue
		seen.add(iso_value)
		normalized.append(iso_value)

	normalized.sort(reverse=True)
	return normalized


# Parse the multiline history field from the edit form into stored dates.
def _parse_history(value: str) -> list[str]:
	if not value.strip():
		return []
	raw_lines = value.replace(",", "\n").splitlines()
	cleaned_values: list[str] = []

	for line in raw_lines:
		stripped = line.strip()
		if not stripped:
			continue
		cleaned_values.append(_parse_date(stripped).isoformat())

	return _normalize_history(cleaned_values)


# Add a month interval to a date while keeping the day valid for the new month.
def _add_months(source_date: date, months: int) -> date:
	total_month = source_date.month - 1 + months
	year = source_date.year + total_month // 12
	month = total_month % 12 + 1
	last_day = calendar.monthrange(year, month)[1]
	day = min(source_date.day, last_day)
	return date(year, month, day)
