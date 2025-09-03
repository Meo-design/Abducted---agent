# social.py
import os
from flask import Blueprint, jsonify

social_bp = Blueprint("social", __name__)

DRAFT_POSTS = [
    "👽 Day 1: A shadow over New Austin… #AbductedMemories",
    "🛸 Two strangers, one glitch in reality. #AbductedMemories",
    "🕳️ Holes in the timeline keep getting wider…",
    "📼 Found footage from the night everything changed.",
    "🧪 When memory becomes a lab experiment…",
    "📡 There's a voice in the signal. It isn’t ours.",
    "🧬 The truth didn’t set us free. It rewired us.",
    "⏳ Time slips are getting longer. We're not coming back clean.",
    "📍 New Austin isn’t on any map. Not the one we know.",
    "🧯 The campaign goes live soon. Stay awake.",
]

def as_bool(val, default=False):
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

def get_dry_run():
    # Read at request time so env changes show up without code edits
    return as_bool(os.getenv("DRY_RUN"), default=False)

def is_social_configured():
    # Consider “configured” only if all X/Twitter creds are present
    required = [
        "SOCIAL_ACCESS_TOKEN",
        "SOCIAL_ACCESS_SECRET",
        "SOCIAL_API_KEY",
        "SOCIAL_API_SECRET",
        "SOCIAL_CLIENT_ID",
        "SOCIAL_CLIENT_SECRET",
    ]
    for k in required:
        v = os.getenv(k)
        if not v or not str(v).strip():
            return False
    return True

@social_bp.route("/", methods=["GET"])
def social_root():
    return jsonify(
        ok=True,
        dry_run=get_dry_run(),
        posts=DRAFT_POSTS,
        social_configured=is_social_configured(),
    )

@social_bp.route("/preview", methods=["GET"])
def social_preview():
    items = "".join(f"<li>{p}</li>" for p in DRAFT_POSTS)
    return f"<h2>Draft Social Posts</h2><ol>{items}</ol>"
