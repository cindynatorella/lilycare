# Backend

This folder now contains a PostgreSQL-ready backend skeleton for LilyCare.

## Files

- `config.py`: reads database settings from environment variables
- `db.py`: connection helpers and future database bootstrap functions
- `models.py`: simple dataclasses for Lily profile, vaccines, history, and vet links
- `pet_repository.py`: starter CRUD function stubs for Lily's profile
- `vaccine_repository.py`: starter CRUD and history function stubs for vaccines
- `vet_repository.py`: starter CRUD function stubs for vet links
- `schema.sql`: initial PostgreSQL tables

## Suggested next steps

1. Install PostgreSQL dependencies from `requirements.txt`.
2. Create the database.
3. Finish `initialize_database()` in `db.py`.
4. Implement the repository functions one file at a time.
5. Update the Flask routes in `frontend/app.py` to call these repository functions instead of using session demo data.
