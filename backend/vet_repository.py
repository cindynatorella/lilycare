from __future__ import annotations

from .models import VetLink


from sqlalchemy import select

from .db import db

# Return every vet link LilyCare should display.
def list_vet_links() -> list[VetLink]:
	statement = (
		select(VetLink)
		.order_by(VetLink.name)
	)

	return list(db.session.scalars(statement).all())


# Return one vet link by id so the edit form can refresh it.
def get_vet_link(vet_id: int) -> VetLink | None:
	return db.session.get(VetLink, vet_id)

# Insert a new vet link row and return the saved record.
def create_vet_link(vet_link: VetLink) -> VetLink:
	db.session.add(vet_link)
	db.session.commit()
	db.session.refresh(vet_link)

	return vet_link


# Update one saved vet link after an edit in the UI.
def update_vet_link(vet_link: VetLink) -> VetLink | None:
	
	saved_vet_link = get_vet_link(vet_link.id)

	if saved_vet_link is None:
		return None

	saved_vet_link.name = vet_link.name
	saved_vet_link.url = vet_link.url
	saved_vet_link.notes = vet_link.notes

	db.session.commit()

	return saved_vet_link


# Delete one saved vet link row.
def delete_vet_link(vet_id: int) -> bool:
	vet = get_vet_link(vet_id)

	if vet is None:
		return False

	db.session.delete(vet)
	db.session.commit()

	return True

