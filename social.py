# social.py
import os
from datetime import datetime

def run(dry_run=True, action="check"):
    x_key = os.getenv("X_BEARER_TOKEN", "unset")          # or TWITTER_BEARER_TOKEN
    fb_key = os.getenv("FB_PAGE_TOKEN", "unset")
    note = "DRY_RUN: not posting anything" if dry_run else "LIVE (be careful)"
    return {
        "module": "social",
        "time": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "status": "ok",
        "creds": {
            "x_bearer_token": "set" if x_key != "unset" else "unset",
            "fb_page_token": "set" if fb_key != "unset" else "unset",
        },
        "message": f"Social module ready. {note}",
        "todo": "Wire real posting to X/Facebook/Instagram here."
    }
