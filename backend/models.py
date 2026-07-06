from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class PetProfile:
    """Represent Lily's single profile row from the database."""

    id: int | None
    name: str
    birth_date: date | None
    description: str


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


@dataclass(slots=True)
class VetLink:
    """Represent one vet link LilyCare can show on the dashboard."""

    id: int | None
    name: str
    url: str
    notes: str
