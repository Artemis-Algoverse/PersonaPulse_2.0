from datetime import datetime
import re

def parse_date(date_str):
    # Implement platform-specific date parsing
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None

def extract_keywords(text):
    # Simple hashtag/keyword extraction
    return re.findall(r'#\w+', text)
