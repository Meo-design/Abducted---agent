# social.py
from flask import Blueprint, jsonify
import os

social_bp = Blueprint("social", __name__)

# --- tiny helpers here to avoid circular imports ---
def as_bool(val, default=False):
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

def get_dry_run():
    return as_bool(os.getenv("DRY_RUN"), default=False)
# ---------------------------------------------------

DRAFT_POSTS = [
    "🛸 Day 1: A shadow over New Austin… #AbductedMemories",
    "🪐 Two strangers, one glitch in reality. #AbductedMemories",
    "🕳️ Holes in the timeline keep getting wider…",
    "📼 Found footage from the night everything changed.",
    "🧪 When memory becomes a lab experiment…",
    "📡 There's a voice in the signal. It isn’t ours.",
    "🧬 The truth didn’t set us free. It rewired us.",
    "⏳ Time slips are getting longer. We're not coming back clean.",
    "📍 New Austin isn’t on any map. Not the one we know.",
    "🚨 The campaign goes live soon. Stay awake.",
]

@social_bp.route("/", methods=["GET"])
def social_root():
    return jsonify(
        ok=True,
        dry_run=get_dry_run(),           # <-- single source of truth
        social_configured=False,         # (will flip to True when keys are validated)
        posts=DRAFT_POSTS
    )

@social_bp.route("/preview", methods=["GET"])
def social_preview():
    items = "".join(f"<li>{p}</li>" for p in DRAFT_POSTS)
    return f"<h2>Draft Social Posts</h2><ol>{items}</ol>"
