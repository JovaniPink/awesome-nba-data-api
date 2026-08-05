# NBA API

> OpenAPI service for NBA data used by measuredstudios.com.

## Features

The service uses:

- [Connexion](https://connexion.readthedocs.io/) to bind the OpenAPI contract to Python handlers.
- [Flask](https://flask.palletsprojects.com/) for the web application.
- [Blueprints](https://flask.palletsprojects.com/en/1.0.x/blueprints/) for scalability.
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/) is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) is a thin integration layer for Flask and marshmallow that adds additional features to marshmallow.
- [SQLAlchemy](https://www.sqlalchemy.org/library.html) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) for database integration.
- [Alembic](http://alembic.zzzcomputing.com/)
- [flask_migrate](https://flask-migrate.readthedocs.io/en/latest/).
- [Tailwind](https://tailwindcss.com/) is a utility-first CSS framework for rapidly building custom user interfaces.

### Code characteristics

- Runs on Python 3.10
- Well organized directories with lots of comments
  - app
    - commands
    - models
    - static
    - templates
    - views
  - test
- Includes test framework (`py.test`)
- Includes database migration framework (`alembic`)

## Installation

### 1. Get the code

    git clone git@github.com:JovaniPink/awesome-nba-data-api.git
    cd awesome-nba-data-api

### 2. Install requirements

    python -m pip install -r requirements.txt

For Docker Compose, create the local environment file first:

    cp .env.example .env

### Initializing the Database

    # Create DB tables and populate sample people
    flask --app manage init-db

### 3. Run the application

For local development:

    python manage.py

#### Running the app (production)

The container runs the Connexion ASGI application with Uvicorn:

    docker compose up --build

#### Running the automated tests

    pytest -q

### Updating dependencies

Edit the direct pins in `requirements.in`, then regenerate the complete lock file with Python 3.10:

    python -m pip install pip-tools
    pip-compile --upgrade --resolver=backtracking --strip-extras --output-file=requirements.txt requirements.in

## Example

### Data Routes

.route('/') # index html file
.route('/api/players')
.route('/api/player/<player_id>')
.route('/api/player/<player_id>/season/<season_id>')
.route('/api/teams')
.route('/api/team/<team_id>')
.route('/api/team/<team_id>/season/<season_id>')
.route('/api/seasons')
.route('/api/season/<season_id>')
.route('/api/game/<date_string>')
Application errors: https://flask.palletsprojects.com/en/stable/errorhandling/

### Model Routes

.route('/api/predict/', methods=['POST']) # Takes in JSON, still figuring out.

## Data Powering the Web app

## Todo Checklist

A helpful checklist to gauge how your README is coming on what I would like to finish:

- [ ] Lots of items! :)
- [ ] Need to add Celery

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
