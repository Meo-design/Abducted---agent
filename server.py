
# server.py
from flask import Flask, jsonify, request
import os

# Import your module files (they can be simple for now)
import amazon_ads
import mailchimp
import social

app = Flask(__name__)

DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ["1", "true", "yes"]

# ---- Home & status ----
@app.route("/")
def home():
    return (
        "<h2>Defenders Autopilot is running ✅</h2>"
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
    return jsonify({"ok": True, "dry_run": DRY_RUN})

# A simple in-memory “last run” cache (resets on redeploy)
LAST = {
    "ads": None,
    "email": None,
    "social": None,
}

@app.route("/dashboard")
def dashboard():
    return jsonify({"status": "online", "last": LAST, "dry_run": DRY_RUN})

# ---- Modules ----
@app.route("/ads")
def ads():
    # Optional query ?action=run to “simulate” a real run
    action = request.args.get("action", "check")
    result = amazon_ads.run(dry_run=DRY_RUN, action=action)
    LAST["ads"] = result
    return jsonify(result)

@app.route("/email")
def email():
    action = request.args.get("action", "check")
    result = mailchimp.run(dry_run=DRY_RUN, action=action)
    LAST["email"] = result
    return jsonify(result)

@app.route("/social")
def social_route():
    action = request.args.get("action", "check")
    result = social.run(dry_run=DRY_RUN, action=action)
    LAST["social"] = result
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

    app.run(host="0.0.0.0", port=8080)
