from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from sqlalchemy import Date, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

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


@dataclass(slots=True)
class VaccineHistoryEntry:
	"""Represent one past administration date for a vaccine."""

	id: int | None
	vaccine_id: int
	administered_on: date


@dataclass(slots=True)
class Vaccine:
	"""Represent one vaccine reminder and its related history."""

	id: int | None
	name: str
	description: str
	note: str
	recurrence_months: int
	next_due: date | None
	history: list[VaccineHistoryEntry] = field(default_factory=list)


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