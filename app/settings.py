# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
APP_NAME = "NBA API"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY", "development-only")

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(os.getcwd(), 'nbaapi.db')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
