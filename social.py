# social.py
import os, random, datetime

# Minimal starter pack (we'll replace with 10 posts after test)
POSTS = [
    "What if your memories weren’t yours to keep? Dive into *Abducted Memories*. #SciFiMystery #LucidDream",
    "He thought it was a dream—until the bullets hit the tarmac. #DreamThriller #AbductedMemories",
    "Surreal, haunting, and metaphysical—memory is currency here. #MetaphysicalFiction #SciFiReads",
]

def run(dry_run=True, action="check"):
    """
    Returns a JSON-like dict describing what would be posted (DRY_RUN=true),
    or confirming a post (DRY_RUN=false, once wired to a real API).
    """
    selected = random.choice(POSTS)
    creds_present = all(os.getenv(k, "").strip() for k in [
        "SOCIAL_API_KEY", "SOCIAL_API_SECRET", "SOCIAL_ACCESS_TOKEN", "SOCIAL_ACCESS_SECRET"
    ])
    return {
        "module": "social",
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "ok",
        "dry_run": bool(dry_run),
        "creds_configured": creds_present,
        "selected_post": selected,
        "action": action,
        "note": "DRY_RUN: no posts sent" if dry_run else "LIVE: (API call not wired yet)"
    }
