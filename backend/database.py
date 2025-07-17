
import sqlite3
import logging
from datetime import datetime

DB_PATH = "events.db"

CREATE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date_time TEXT,
    location TEXT,
    link TEXT UNIQUE,
    attending_count INTEGER,
    is_online BOOLEAN,
    is_free BOOLEAN,
    is_paid BOOLEAN,
    keywords TEXT,
    platform TEXT,
    created_at TEXT
);
'''

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        conn.commit()
    logging.info("SQLite database and events table ready.")

def remove_expired_events():
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM events WHERE date_time < ?", (now,))
        deleted = cur.rowcount
        conn.commit()
    logging.info(f"Expired events removed: {deleted}")

def insert_events(events):
    if not events:
        logging.info("No events to insert.")
        return
    with get_connection() as conn:
        cur = conn.cursor()
        for e in events:
            # Convert keywords list to comma-separated string
            keywords = ','.join(e.get('keywords', [])) if isinstance(e.get('keywords'), list) else (e.get('keywords') or '')
            # Try to update if exists, else insert
            try:
                cur.execute("SELECT * FROM events WHERE link = ?", (e['link'],))
                existing = cur.fetchone()
                if existing:
                    cur.execute("""
                        UPDATE events SET title=?, date_time=?, location=?, attending_count=?, is_online=?, is_free=?, is_paid=?, keywords=?, platform=?, created_at=? WHERE link=?
                    """, (
                        e['title'], str(e['date_time']), e['location'], e.get('attending_count'),
                        int(e['is_online']), int(e['is_free']), int(e['is_paid']), keywords, e['platform'], str(e['created_at']), e['link']
                    ))
                    logging.info(f"Event updated: {e['title']}")
                else:
                    cur.execute("""
                        INSERT INTO events (title, date_time, location, link, attending_count, is_online, is_free, is_paid, keywords, platform, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        e['title'], str(e['date_time']), e['location'], e['link'], e.get('attending_count'),
                        int(e['is_online']), int(e['is_free']), int(e['is_paid']), keywords, e['platform'], str(e['created_at'])
                    ))
                    logging.info(f"Event added: {e['title']}")
            except Exception as ex:
                logging.error(f"Error inserting/updating event {e.get('title')}: {ex}")
        conn.commit()
