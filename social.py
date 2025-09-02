# social.py
from flask import Blueprint, jsonify

social_bp = Blueprint("social", __name__)

DRAFT_POSTS = [
    "👽 Day 1: A shadow over New Austin… #AbductedMemories",
    "🛸 Two strangers, one glitch in reality. #AbductedMemories",
    "🕳️ Holes in the timeline keep getting wider…",
    "📼 Found footage from the night everything changed.",
    "🧪 When memory becomes a lab experiment…",
    "🌌 There's a voice in the signal. It isn’t ours.",
    "🔦 The truth didn’t set us free. It rewired us.",
    "⏳ Time slips are getting longer. We're not coming back clean.",
    "📍 New Austin isn’t on any map. Not the one we know.",
    "🚨 The campaign goes live soon. Stay awake."
]

@social_bp.route("/", methods=["GET"])
def social_root():
    return jsonify(
        ok=True,
        dry_run=True,
        social_configured=False,
        posts=DRAFT_POSTS
    )

@social_bp.route("/preview", methods=["GET"])
def social_preview():
    items = "".join(f"<li>{p}</li>" for p in DRAFT_POSTS)
    return f"<h2>Draft Social Posts</h2><ol>{items}</ol>"
