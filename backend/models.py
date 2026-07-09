from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from sqlalchemy import Date, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import db

class PetProfile(db.Model):
	"""Represent Lily's single profile row from the database."""

	__tablename__ = "pet_profiles"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(Text, nullable=False)
	birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
	description: Mapped[str] = mapped_column(Text, nullable=False, default="")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"birth_date": self.birth_date.isoformat() if self.birth_date else None,
			"description": self.description,
		}


class VaccineHistoryEntry(db.Model):
	"""Represent one past administration date for a vaccine."""

	__tablename__ = "vaccine_history_entries"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	vaccine_id: Mapped[int] = mapped_column(
		ForeignKey("vaccines.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	administered_on: Mapped[date] = mapped_column(Date, nullable=False)

	vaccine: Mapped["Vaccine"] = relationship(back_populates="history")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"vaccine_id": self.vaccine_id,
			"administered_on": self.administered_on.isoformat(),
		}


class Vaccine(db.Model):
	"""Represent one vaccine reminder and its related history."""

	__tablename__ = "vaccines"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(Text, nullable=False)
	description: Mapped[str] = mapped_column(Text, nullable=False, default="")
	note: Mapped[str] = mapped_column(Text, nullable=False, default="")
	recurrence_months: Mapped[int] = mapped_column(Integer, nullable=False)
	next_due: Mapped[date | None] = mapped_column(Date, nullable=True)

	history: Mapped[list[VaccineHistoryEntry]] = relationship(
		back_populates="vaccine",
		cascade="all, delete-orphan",
		order_by=lambda: VaccineHistoryEntry.administered_on.desc(),
	)

	def to_dict(self) -> dict:
		history_values = [
			entry.administered_on.isoformat()
			for entry in self.history
		]

		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"note": self.note,
			"recurrence_months": self.recurrence_months,
			"next_due": self.next_due.isoformat() if self.next_due else "",
			"last_given": history_values[0] if history_values else "",
			"history": history_values,
		}


class VetLink(db.Model):
	"""Represent one vet link LilyCare can show on the dashboard."""

	__tablename__ = "vet_links"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(Text, nullable=False, default="")
	url: Mapped[str] = mapped_column(Text, nullable=False, default="")
	notes: Mapped[str] = mapped_column(Text, nullable=False, default="")

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"url": self.url,
			"notes": self.notes,
		}


class AppAccessConfig(db.Model):
	"""Store the shared app password hash for the login gate."""

	__tablename__ = "app_access_config"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
	password_hash: Mapped[str] = mapped_column(Text, nullable=False)
