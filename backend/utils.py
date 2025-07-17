from datetime import datetime
import re
from dateutil import parser

# Parse date from various formats (platform-specific)
def parse_date(date_str):
    if not date_str:
        return None
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str)
    except Exception:
        pass
    try:
        # Try dateutil parser for flexible formats
        return parser.parse(date_str, fuzzy=True)
    except Exception:
        return None

# Extract hashtags and keywords from text
def extract_keywords(text):
    if not text:
        return []
    hashtags = re.findall(r'#\w+', text)
    # Also extract words longer than 3 chars as keywords
    words = re.findall(r'\b\w{4,}\b', text)
    return list(set(hashtags + words))

# Clean and normalize event title
def clean_title(title):
    if not title:
        return ""
    return re.sub(r'\s+', ' ', title).strip()

# Check if event is free or paid
def is_event_free(text):
    if not text:
        return True
    return bool(re.search(r'free|complimentary|no charge', text, re.IGNORECASE))

# Check if event is online or offline
def is_event_online(text):
    if not text:
        return False
    return bool(re.search(r'online|virtual|webinar|zoom', text, re.IGNORECASE))

# Extract footfall/attending count if present
def extract_attending_count(text):
    if not text:
        return 0
    match = re.search(r'(\d{2,})\s*(attending|participants|RSVP)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0
