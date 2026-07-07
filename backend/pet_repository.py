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
	saved_profile = get_pet_profile()

	if saved_profile is None:
		saved_profile = PetProfile(
			name=profile.name,
			birth_date=profile.birth_date,
			description=profile.description,
		)

		db.session.add(saved_profile) # Adds if it does not exist.
	else:
		saved_profile.birth_date = profile.birth_date
		saved_profile.description = profile.description

	db.session.commit() # Alchemy creates the update or add for me 

	return saved_profile
