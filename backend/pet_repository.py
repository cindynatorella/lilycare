from __future__ import annotations

from .models import PetProfile


# Fetch Lily's single saved profile from PostgreSQL.
def get_pet_profile() -> PetProfile | None:
    raise NotImplementedError("TODO: Select Lily's profile row and return it as a PetProfile.")


# Create Lily's profile row when the database is empty.
def create_pet_profile(profile: PetProfile) -> PetProfile:
    raise NotImplementedError("TODO: Insert Lily's profile and return the saved PetProfile.")


# Update Lily's profile fields after an edit in the Flask UI.
def update_pet_profile(profile: PetProfile) -> PetProfile:
    raise NotImplementedError("TODO: Update Lily's profile row and return the saved PetProfile.")
