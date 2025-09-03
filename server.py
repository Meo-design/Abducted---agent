# server.py
from flask import Flask, jsonify
import logging

def as_bool(val, default=False):
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "y", "on")

def get_dry_run():
    # Always re-check the env var when called
    return as_bool(os.getenv("DRY_RUN"), default=False)

# Log once at boot what we see in the env
logging.basicConfig(level=logging.INFO)
logging.info("Boot config -> DRY_RUN raw=%r parsed=%s",
             os.getenv("DRY_RUN"), as_bool(os.getenv("DRY_RUN"), default=False))
 social import social_bp  # import the blueprint

app = Flask(__name__)         # create the Flask app

# register the blueprint AFTER app exists
app.register_blueprint(social_bp, url_prefix="/social")


@app.route("/")
def home():
    return (
        "<h2>Defenders Autopilot is running ✅</h2>"
        "<p>Try:</p>"
        "<ul>"
        "<li><a href='/health'>/health</a></li>"
        "<li><a href='/dashboard'>/dashboard</a></li>"
        "<li><a href='/social'>/social</a> (JSON)</li>"
        "<li><a href='/social/preview'>/social/preview</a> (HTML)</li>"
        "</ul>"
    )


@app.route("/health")
def health():
    return jsonify(ok=True)


@app.route("/dashboard")
def dashboard():
    return jsonify(status="online", message="Dashboard placeholder")


# local run only (ignored on Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

