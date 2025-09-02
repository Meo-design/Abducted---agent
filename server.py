f# server.py
from flask import Flask, jsonify
from social import social_bp          # 1) import blueprint

app = Flask(__name__)                 # 2) create app

# ... any other setup (env, logging, etc.) ...

app.register_blueprint(social_bp, url_prefix="/social")  # 3) register blueprint AFTER app exists


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

# local debug only (Render ignores this)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
