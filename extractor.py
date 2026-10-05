"""Week 2 homework: fix the date extractor.

Our event bot reads show notices and puts the EVENT date on the calendar.
Right now it grabs the first date it sees, which is often the RSVP deadline.

Your job: change extract_event_date() so it returns the date of the event itself.
Only edit this file. Run the tests with:  python -m unittest -v
"""

import re
from datetime import datetime

NOTICE = (
    "BK UNDERGROUND SESSIONS #12: Presale RSVP lottery drops October 14, 2026 at 6:00 PM online. "
    "Secret warehouse doors open October 21, 2026 at 11:00 PM for the live set. "
    "Curfew strictly midnight. 21+ only."
)

DATE_PATTERN = r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})"

# Keywords that indicate a date is a deadline or pre-sale rather than the event itself
IGNORE_KEYWORDS = ["rsvp", "presale", "pre-sale", "lottery", "closes", "by", "deadline", "until", "ends"]


def to_iso(match):
    """Turn a regex match like 'October 21, 2026' into '2026-10-21'."""
    return datetime.strptime(match.group(0), "%B %d, %Y").strftime("%Y-%m-%d")


def extract_event_date(text):
    """Return the event date as 'YYYY-MM-DD', or None if the notice has no event date."""
    if not text:
        return None

    # Inspect each date match in order
    for match in re.finditer(DATE_PATTERN, text):
        start, end = match.span()

        # Grab ~40 characters BEFORE the date match
        context = text[max(0, start - 40):start].lower()

        # Skip this date if it is tied to an RSVP or deadline keyword
        if any(keyword in context for keyword in IGNORE_KEYWORDS):
            continue

        # Return the first valid event date using your original to_iso helper
        return to_iso(match)

    return None

if __name__ == "__main__":
    print("Event date:", extract_event_date(NOTICE))