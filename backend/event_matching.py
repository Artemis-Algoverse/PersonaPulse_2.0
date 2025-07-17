import re
import sqlite3
import logging

DB_PATH = 'events.db'

# Extract keywords from event title, description, tags
def extract_event_keywords(title, description, tags=None):
    text = f"{title} {description} " + (tags if tags else '')
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    words = text.split()
    keywords = [w for w in words if len(w) > 2]
    return ','.join(sorted(set(keywords)))

# Update keywords column for all events
def update_event_keywords():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, keywords FROM events")
    events = cur.fetchall()
    for eid, title, desc, old_kw in events:
        new_kw = extract_event_keywords(title or '', desc or '', old_kw)
        cur.execute("UPDATE events SET keywords=? WHERE id=?", (new_kw, eid))
    conn.commit()
    conn.close()
    logging.info("Event keywords updated for all events.")

if __name__ == '__main__':
    update_event_keywords()
    print("Event keywords extraction complete.")
