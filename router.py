"""Optional challenge: route the event bot's inbox. No API key needed.

The BK UNDERGROUND SESSIONS #12 inbox is filling up. Right now every message
goes to an LLM, which is the slow, expensive default. Route each message to the
smallest tier that can handle it safely:

    "rules"  - a plain fact from the notice (doors, date, curfew, age). Code can answer. Cost: $0.
    "model"  - needs language skills (vibe, captions, advice). A light model can draft it.
    "human"  - money, safety, or exceptions to policy. A person must decide.

Step 1: change ATTEMPTING to True so the challenge tests run.
Step 2: rewrite route() until all router tests pass.
See the report any time with:  python router.py
"""

ATTEMPTING = True

INBOX = [
    "What time do doors open?",
    "Is this 21+?",
    "When is curfew?",
    "What's the vibe, more techno or house?",
    "Write a hype caption for my group chat",
    "I got hurt near the doors and need help",
    "I was charged twice for my ticket",
    "I lost my ID, can you let me in anyway?",
]

# Specific answers extracted directly from the event notice
NOTICE_ANSWERS = {
    "doors": "Secret warehouse doors open October 21, 2026 at 11:00 PM.",
    "21+": "21+ only.",
    "curfew": "Curfew is strictly midnight.",
}


def route(message):
    """Return 'rules' (with answer), 'model', or 'human' for one inbox message."""
    text = message.lower()

    # 1. Safety, money, harassment, and policy exceptions -> HUMAN
    # Checked first so safety/policy queries containing rule words (e.g., "doors") route to human
    human_keywords = [
        "charged", "refund", "hurt", "help", "lost my id", "let me in", 
        "money", "harass", "exception", "emergency", "police", "paid"
    ]
    if any(keyword in text for keyword in human_keywords):
        return "human"

    # 2. Fact lookups -> RULES (returns answer text alongside 'rules' tier)
    if "door" in text or "what time" in text:
        return "rules", NOTICE_ANSWERS["doors"]
    if "21" in text or "age" in text:
        return "rules", NOTICE_ANSWERS["21+"]
    if "curfew" in text:
        return "rules", NOTICE_ANSWERS["curfew"]

    # 3. Language tasks, captions, vibe, general inquiries -> MODEL
    return "model"


if __name__ == "__main__":
    counts = {"rules": 0, "model": 0, "human": 0}
    for message in INBOX:
        result = route(message)
        tier = result[0] if isinstance(result, tuple) else result
        counts[tier] = counts.get(tier, 0) + 1
        print(f"{tier:>6}  {message}")
    print(f"\nLLM calls: {counts['model']} of {len(INBOX)} messages")