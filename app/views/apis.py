from flask import Blueprint, jsonify

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint("api", __name__, template_folder="templates")


@api_blueprint.route("/nbadata", methods=["GET"])
def nbadata():
    ret = {"sample return": 10}
    return (jsonify(ret), 200)
