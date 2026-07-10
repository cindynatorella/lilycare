from frontend import create_app
import os

app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("APP_ENV") != "production")
