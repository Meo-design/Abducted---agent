# server.py
from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)

# ---------- helpers ----------
def env_bool(name: str, default: bool = True) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "on"}

def present(*names) -> bool:
    """True if all named env vars are non-empty."""
    for n in names:
        if not os.getenv(n, "").strip():
            return False
    return True

def config_snapshot():
    return {
        "dry_run": env_bool("DRY_RUN", True),
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "amazon_configured": present(
            "AMAZON_CLIENT_ID", "AMAZON_CLIENT_SECRET",
            "AMAZON_REFRESH_TOKEN", "AMAZON_PROFILE_ID"
        ),
        "mailchimp_configured": present(
            "MAILCHIMP_API_KEY", "MAILCHIMP_SERVER_PREFIX", "MAILCHIMP_LIST_ID"
        ),
        "social_configured": present(
            "SOCIAL_API_KEY", "SOCIAL_API_SECRET",
            "SOCIAL_ACCESS_TOKEN", "SOCIAL_ACCESS_SECRET"
        ),
    }

# set log level from env (optional)
logging.getLogger().setLevel(
    {"debug": logging.DEBUG, "info": logging.INFO,
     "warning": logging.WARNING, "error": logging.ERROR}.get(
        os.getenv("LOG_LEVEL", "info").lower(), logging.INFO)
)

# ---------- routes ----------
@app.route("/")
def home():
    return (
        "<h1>Defenders Autopilot is running ✅</h1>"
        "<p>Try:</p>"
        "<ul>"
        "<li><a href='/health'>/health</a></li>"
        "<li><a href='/dashboard'>/dashboard</a></li>"
        "<li><a href='/ads'>/ads</a> (Amazon Ads check/run)</li>"
        "<li><a href='/email'>/email</a> (Mailchimp check/send)</li>"
        "<li><a href='/social'>/social</a> (Social check/post)</li>"
        "</ul>"
    )

@app.route("/health")
def health():
    cfg = config_snapshot()
    return jsonify({"ok": True, **cfg})

@app.route("/dashboard")
def dashboard():
    cfg = config_snapshot()
    return jsonify({
        "status": "online",
        "message": "Dashboard placeholder",
        **cfg
    })

@app.route("/ads")
def ads():
    cfg = config_snapshot()
    if not cfg["amazon_configured"]:
        return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                        "amazon_configured": False,
                        "note": "Set AMAZON_* vars to activate."})
    return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                    "amazon_configured": True,
                    "action": "would check/adjust bids here"})

@app.route("/email")
def email():
    cfg = config_snapshot()
    if not cfg["mailchimp_configured"]:
        return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                        "mailchimp_configured": False,
                        "note": "Set MAILCHIMP_* vars to activate."})
    return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                    "mailchimp_configured": True,
                    "action": "would send/list campaign here"})

@app.route("/social")
def social():
    cfg = config_snapshot()
    if not cfg["social_configured"]:
        return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                        "social_configured": False,
                        "note": "Set SOCIAL_* vars to activate."})
    return jsonify({"ok": True, "dry_run": cfg["dry_run"],
                    "social_configured": True,
                    "action": "would post scheduled content here"})

# local dev only; Render uses Gunicorn in Dockerfile
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
