# server.py
import os
import logging
from flask import Flask, jsonify
from social import social_bp  # import the blueprint (must be line-with no leading spaces)

def as_bool(val, default=False):
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

def get_dry_run():
    # Always re-read the env on each request (we also log what we saw at boot)
    return as_bool(os.getenv("DRY_RUN"), default=False)

# ---- log the boot-time view of DRY_RUN so the logs prove what the app saw ----
logging.basicConfig(level=logging.INFO)
logging.info(
    "Boot config -> DRY_RUN raw=%r parsed=%s",
    os.getenv("DRY_RUN"),
    as_bool(os.getenv("DRY_RUN"), default=False),
)
# -----------------------------------------------------------------------------

app = Flask(__name__)

# Register blueprint at /social
app.register_blueprint(social_bp, url_prefix="/social")

@app.route("/")
def home():
    return (
        "<h2>Defenders Autopilot is running ✅</h2>"
        "<p>Try:</p>"
        "<ul>"
        '<li><a href="/health">/health</a></li>'
        '<li><a href="/dashboard">/dashboard</a></li>'
        '<li><a href="/social/">/social</a> (JSON)</li>'
        '<li><a href="/social/preview">/social/preview</a> (HTML)</li>'
        "</ul>"
    )

@app.route("/dashboard")
def dashboard():
    return jsonify({"message": "Dashboard placeholder", "status": "online"})

@app.route("/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
