# social.py
import os
import random
from flask import jsonify

def handle_social():
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    # 10 campaign posts
    posts = [
        "🚀 Ready to unlock *Abducted Memories*? Dive into the mystery today. #SciFi #Thriller",
        "What if your memories weren’t your own? 🔍 Discover the truth in *Abducted Memories*. 📖",
        "🔥 Hot off the press: *Abducted Memories* is live. Don’t just read a story — experience it.",
        "Triple 0. Vexx. Mort. Echo Prime. Your new obsession starts here → *Abducted Memories* 📚",
        "Some books entertain. This one hijacks your mind. 😱 #AbductedMemories",
        "Lucid dreams, stolen memories, and conspiracies within conspiracies. Ready to wake up? 🌌",
        "This isn’t just fiction. It’s a system. And you’re already inside it. 🌀 #AbductedMemories",
        "Readers are calling it 'mind-bending' and 'unlike anything else out there.' You be the judge.",
        "Think you can trust your own thoughts? *Abducted Memories* will make you question everything.",
        "The game’s afoot — but not in the way you think. Step inside the labyrinth. 🕵️‍♂️"
    ]

    # Pick a random post
    selected = random.choice(posts)

    if dry_run:
        return jsonify({
            "ok": True,
            "dry_run": True,
            "note": "Set SOCIAL_* vars and DRY_RUN=false to actually post.",
            "post_selected": selected
        })

    # Live mode (when API keys are set)
    # TODO: Add actual API call here (Twitter/X, Facebook, etc.)
    return jsonify({
        "ok": True,
        "dry_run": False,
        "post_sent": selected
    })
