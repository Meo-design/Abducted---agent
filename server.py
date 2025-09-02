
# server.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return (
        "<h2>Defenders Autopilot is running ✅</h2>"
        "<p>Try:</p>"
        "<ul>"
        "<li><a href='/health'>/health</a></li>"
        "<li><a href='/dashboard'>/dashboard</a></li>"
        "</ul>"
    )

@app.route("/health")
def health():
    return jsonify({"ok": True})

@app.route("/dashboard")
def dashboard():
    # minimal placeholder; you can render recent logs/results here later
    return jsonify({"status": "online", "message": "Dashboard placeholder"})

# Optional: local run (ignored on Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
