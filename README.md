# LilyCare
Pet health and vaccine reminder app for Lily, built with Python and Flask.

## Current focus
The project now includes a frontend-first Flask dashboard with:

- Lily's single-pet profile card
- Vaccine reminder cards with current, due soon, and overdue states
- Toggle-to-edit forms so the page stays simple until you want to change something
- Clickable vet scheduling shortcuts

The data is temporary for now so we can shape the UI before wiring up PostgreSQL.

## Run the app
1. Create or repair a local virtual environment with Python 3.12+.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the Flask app:

```powershell
python app.py
```

4. Open `http://127.0.0.1:5000`.


5. Don't forget to connect the DB.