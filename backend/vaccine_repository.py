from __future__ import annotations

from datetime import date

from sqlalchemy import delete, select

from .db import db
from .models import Vaccine, VaccineHistoryEntry


# Return every vaccine reminder LilyCare should display.
def list_vaccines() -> list[Vaccine]:
	statement = (
		select(Vaccine)
		.order_by(Vaccine.name)
	)

	return list(db.session.scalars(statement).all())


# Return one vaccine by id so the UI can edit or refresh a single record.
def get_vaccine(vaccine_id: int) -> Vaccine | None:
	return db.session.get(Vaccine, vaccine_id)


# Insert a new vaccine reminder row and return the saved vaccine.
def create_vaccine(vaccine: Vaccine) -> Vaccine:
	db.session.add(vaccine)
	db.session.commit()
	db.session.refresh(vaccine)

	return vaccine


# Update a vaccine's main fields such as note, recurrence, and next due date.
def update_vaccine(vaccine: Vaccine) -> Vaccine | None:
	if vaccine.id is None:
		return None

	saved_vaccine = get_vaccine(vaccine.id)

	if saved_vaccine is None:
		return None

	saved_vaccine.name = vaccine.name
	saved_vaccine.description = vaccine.description
	saved_vaccine.note = vaccine.note
	saved_vaccine.recurrence_months = vaccine.recurrence_months
	saved_vaccine.next_due = vaccine.next_due

	db.session.commit()

	return saved_vaccine


# Delete a vaccine and any related history entries from PostgreSQL.
def delete_vaccine(vaccine_id: int) -> bool:
	vaccine = get_vaccine(vaccine_id)

	if vaccine is None:
		return False

	db.session.delete(vaccine)
	db.session.commit()

	return True


# Replace all saved history entries for one vaccine with the edited list from the UI.
def replace_vaccine_history(vaccine_id: int, history: list[date]) -> list[VaccineHistoryEntry]:
	vaccine = get_vaccine(vaccine_id)

	if vaccine is None:
		return []

	unique_dates = sorted(set(history), reverse=True)

	db.session.execute(
		delete(VaccineHistoryEntry)
		.where(VaccineHistoryEntry.vaccine_id == vaccine_id)
	)

	db.session.flush()

	new_entries = [
		VaccineHistoryEntry(
			vaccine_id=vaccine_id,
			administered_on=administered_on,
		)
		for administered_on in unique_dates
	]

	db.session.add_all(new_entries)
	db.session.commit()

	return new_entries


# Add one new administration date when a vaccine is marked completed.
def add_vaccine_history_entry(vaccine_id: int, administered_on: date) -> VaccineHistoryEntry | None:
	vaccine = get_vaccine(vaccine_id)

	if vaccine is None:
		return None

	existing_entry = db.session.scalars(
		select(VaccineHistoryEntry)
		.where(VaccineHistoryEntry.vaccine_id == vaccine_id)
		.where(VaccineHistoryEntry.administered_on == administered_on)
	).first()

	if existing_entry is not None:
		return existing_entry

	new_entry = VaccineHistoryEntry(
		vaccine_id=vaccine_id,
		administered_on=administered_on,
	)

	db.session.add(new_entry)
	db.session.commit()
	db.session.refresh(new_entry)

	return new_entry