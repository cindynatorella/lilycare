from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta


# Seed the app with a starter Lily profile and sample reminder data.
def build_default_state() -> dict:
    today = date.today()

    return deepcopy(
        {
            "profile": {
                "name": "Lily",
                "birth_date": "2021-05-12",
                "description": (
                    "Lily is a playful, treat-motivated pup who does best with a calm "
                    "routine, short reminders, and plenty of post-appointment praise."
                ),
            },
            "vaccines": [
                {
                    "id": "rabies",
                    "name": "Rabies",
                    "description": "Required core vaccine for rabies protection.",
                    "note": "Bring Lily's printed county tag paperwork to the appointment.",
                    "recurrence_months": 12,
                    "next_due": (today + timedelta(days=146)).isoformat(),
                    "last_given": (today - timedelta(days=219)).isoformat(),
                    "history": [
                        (today - timedelta(days=219)).isoformat(),
                        (today - timedelta(days=584)).isoformat(),
                    ],
                },
                {
                    "id": "bordetella",
                    "name": "Bordetella",
                    "description": "Helpful for boarding, grooming, and daycare visits.",
                    "note": "Useful to keep current before any boarding weekends.",
                    "recurrence_months": 12,
                    "next_due": (today + timedelta(days=18)).isoformat(),
                    "last_given": (today - timedelta(days=347)).isoformat(),
                    "history": [
                        (today - timedelta(days=347)).isoformat(),
                        (today - timedelta(days=712)).isoformat(),
                    ],
                },
                {
                    "id": "dhpp",
                    "name": "DHPP",
                    "description": "Core combo vaccine covering distemper, hepatitis, parvo, and parainfluenza.",
                    "note": "Ask whether the vet wants to pair this with Lily's wellness exam.",
                    "recurrence_months": 12,
                    "next_due": (today - timedelta(days=12)).isoformat(),
                    "last_given": (today - timedelta(days=377)).isoformat(),
                    "history": [
                        (today - timedelta(days=377)).isoformat(),
                        (today - timedelta(days=742)).isoformat(),
                    ],
                },
            ],
            "vets": [
                {
                    "id": "main-clinic",
                    "name": "LilyCare Animal Clinic",
                    "url": "https://example.com/book-lily",
                    "notes": "Primary care and annual vaccine appointments.",
                },
                {
                    "id": "urgent-care",
                    "name": "Neighborhood Pet Urgent Care",
                    "url": "https://example.com/urgent-care",
                    "notes": "Backup option for quick follow-up scheduling.",
                },
            ],
        }
    )
