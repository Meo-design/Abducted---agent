@app.route("/social")
def social():
    dry_run = True  # always safe until API keys are added
    configured = False

    # Example: 10 draft posts
    draft_posts = [
        "🚀 Abducted Memories is live — a mind-bending thriller you won’t put down. #SciFi #Thriller",
        "What happens when memories are stolen, sold, and weaponized? 🔥 #AbductedMemories",
        "Triple 0 is back — and reality itself is the battlefield. 📚⚡",
        "Defenders Autopilot online ✅ Time to spread the word. #Automation #IndieAuthor",
        "Would you sell your past to save your future? That’s the question at the heart of Abducted Memories.",
        "Glitching androids, stolen dreams, and a fight against Echo Prime — your new obsession awaits.",
        "Some books entertain. This one hacks your brain. 🧠 #Cyberpunk #NewRelease",
        "Calling all sci-fi lovers: the game changes here. #AbductedMemories #Thriller",
        "You’ve never read a novel like this — because no one’s dared to write one. Until now.",
        "💡 Thought experiment: If your identity could be stolen, how would you fight to get it back?"
    ]

    return jsonify({
        "ok": True,
        "dry_run": dry_run,
        "social_configured": configured,
        "generated_posts": draft_posts
    })
