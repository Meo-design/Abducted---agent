from flask import Blueprint, jsonify

social_bp = Blueprint("social", __name__)

@social_bp.route("/", methods=["GET"])
def social_root():
    # returns JSON with draft posts
    ...

@social_bp.route("/preview", methods=["GET"])
def social_preview():
    # returns HTML list of posts
    ...
