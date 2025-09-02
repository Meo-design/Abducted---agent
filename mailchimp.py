# mailchimp.py
import os
from datetime import datetime

def run(dry_run=True, action="check"):
    api_key = os.getenv("MAILCHIMP_API_KEY", "unset")
    audience = os.getenv("MAILCHIMP_AUDIENCE_ID", "unset")
    note = "DRY_RUN: not sending any emails" if dry_run else "LIVE (be careful)"
    return {
        "module": "mailchimp",
        "time": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "audience_id": audience,
        "status": "ok",
        "message": f"Mailchimp module ready. {note}",
        "todo": "Wire a real campaign or newsletter send here."
    }
