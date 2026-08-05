from flask import Blueprint, redirect, render_template, current_app
from flask import (
    request,
    url_for,
    flash,
    send_from_directory,
    jsonify,
    render_template_string,
)
from flask_login import current_user, login_required

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint("main", __name__, template_folder="templates")


@main_blueprint.route("/")
def member_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))

    return render_template("pages/global.html")


@main_blueprint.route("/home")
@login_required
def home_page():
    return render_template("pages/home.html")
