"""NBA API application factory and extension ownership."""

import os

import connexion
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(_user_id):
    """Return no user until the API defines a persistent user model."""
    return


def create_app(extra_config_settings=None):
    """Create the Connexion application and its underlying Flask app."""
    connexion_app = connexion.FlaskApp(__name__, specification_dir=basedir)
    app = connexion_app.app

    app.config.from_object("app.settings")
    if os.path.exists(os.path.join(basedir, "local_settings.py")):
        app.config.from_object("app.local_settings")
    app.config.update(extra_config_settings or {})

    connexion_app.add_api("swagger.yaml")

    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register model metadata before CLI commands or tests call db.create_all().
    from app.models import nba_models  # noqa: F401
    from app.views.apis import api_blueprint
    from app.views.landing import main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)

    return connexion_app
