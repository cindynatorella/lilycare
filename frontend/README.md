# Frontend

The frontend lives in Flask templates and CSS.

## Included

- `frontend/app.py`: routes and session-backed demo behavior
- `frontend/templates/`: Jinja templates for the LilyCare dashboard
- `frontend/static/styles.css`: custom styling for the app

This layer is intentionally lightweight so we can later connect the forms and cards to a PostgreSQL-backed backend without redesigning the interface.
