from __future__ import annotations

from datetime import date

from .models import Vaccine, VaccineHistoryEntry


# Return every vaccine LilyCare should show on the dashboard.
def list_vaccines() -> list[Vaccine]:
    raise NotImplementedError("TODO: Select all vaccines and attach their history entries.")


# Return one vaccine by id so the UI can edit or refresh a single record.
def get_vaccine(vaccine_id: int) -> Vaccine | None:
    raise NotImplementedError("TODO: Select one vaccine and its history by vaccine_id.")


# Insert a new vaccine reminder row and return the saved vaccine.
def create_vaccine(vaccine: Vaccine) -> Vaccine:
    raise NotImplementedError("TODO: Insert a vaccine row, then save any history entries it includes.")


# Update a vaccine's main fields such as note, recurrence, and next due date.
def update_vaccine(vaccine: Vaccine) -> Vaccine:
    raise NotImplementedError("TODO: Update the vaccine row and return the saved vaccine.")


# Delete a vaccine and any related history entries from PostgreSQL.
def delete_vaccine(vaccine_id: int) -> None:
    raise NotImplementedError("TODO: Delete the vaccine row and cascade or remove its history rows.")


# Replace all saved history entries for one vaccine with the edited list from the UI.
def replace_vaccine_history(vaccine_id: int, history: list[date]) -> list[VaccineHistoryEntry]:
    raise NotImplementedError("TODO: Clear old history rows for the vaccine and insert the new dates.")


# Add one new administration date when a vaccine is marked completed.
def add_vaccine_history_entry(vaccine_id: int, administered_on: date) -> VaccineHistoryEntry:
    raise NotImplementedError("TODO: Insert one history row for the provided vaccine and date.")
