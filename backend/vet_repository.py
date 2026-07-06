from __future__ import annotations

from .models import VetLink


# Return every vet link LilyCare should display.
def list_vet_links() -> list[VetLink]:
    raise NotImplementedError("TODO: Select all saved vet links ordered however you prefer.")


# Return one vet link by id so the edit form can refresh it.
def get_vet_link(vet_id: int) -> VetLink | None:
    raise NotImplementedError("TODO: Select a single vet link by vet_id.")


# Insert a new vet link row and return the saved record.
def create_vet_link(vet_link: VetLink) -> VetLink:
    raise NotImplementedError("TODO: Insert the vet link row and return the saved VetLink.")


# Update one saved vet link after an edit in the UI.
def update_vet_link(vet_link: VetLink) -> VetLink:
    raise NotImplementedError("TODO: Update the vet link row and return the saved VetLink.")


# Delete one saved vet link row.
def delete_vet_link(vet_id: int) -> None:
    raise NotImplementedError("TODO: Delete the matching vet link row.")
