from __future__ import annotations

from .models import PetProfile

from sqlalchemy import select

from .db import db

# Fetch Lily's single saved profile from PostgreSQL.
def get_pet_profile() -> PetProfile | None:
	statement = (
		select(PetProfile)
		.where(PetProfile.name == "Lily")
		.limit(1)
	)

	return db.session.execute(statement).scalar_one_or_none()


# Create Lily's profile row when the database is empty.
def create_pet_profile(profile: PetProfile) -> PetProfile:
    raise NotImplementedError("TODO: Insert Lily's profile and return the saved PetProfile.")


# Update Lily's profile fields after an edit in the Flask UI.
def update_pet_profile(profile: PetProfile) -> PetProfile:
    raise NotImplementedError("TODO: Update Lily's profile row and return the saved PetProfile.")
