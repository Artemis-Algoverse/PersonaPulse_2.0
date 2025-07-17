
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from database import setup_database, insert_events, remove_expired_events, get_connection
from fetch_devpost import fetch_devpost
from fetch_eventbrite import fetch_eventbrite
from fetch_meraevents import fetch_meraevents

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def deduplicate_events(events):
    seen = set()
    deduped = []
    for e in events:
        key = (e.get('title','').lower(), e.get('url','') or e.get('link',''))
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    return deduped

def run_all_scrapers():
    all_events = []
    for fetcher, name in [
        (fetch_devpost, "Devpost"),
        (fetch_eventbrite, "Eventbrite"),
        (fetch_meraevents, "MeraEvents")
    ]:
        logging.info(f"Fetching events from {name}...")
        try:
            events = fetcher()
            logging.info(f"Fetched {len(events)} events from {name}.")
            all_events.extend(events)
        except Exception as ex:
            logging.error(f"Error fetching from {name}: {ex}")
    return deduplicate_events(all_events)

def insert_and_report_events(events):
    if not events:
        print("❌ No events to add to database.")
        return
    insert_events(events)
    print(f"✅ {len(events)} events added/updated in event.db!")
    # Show a sample of events from DB
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, date_time, location, link FROM events ORDER BY created_at DESC LIMIT 10")
        rows = cur.fetchall()
        print("\n📋 Sample events in database:")
        for row in rows:
            print(f"--> {row[0]} | {row[1]} | {row[2]} | {row[3]}")

def job():
    logging.info("Scheduled job started.")
    remove_expired_events()
    events = run_all_scrapers()
    if not events:
        logging.warning("No events fetched from any site.")
    else:
        logging.info(f"Total events fetched: {len(events)}")
    insert_and_report_events(events)
    logging.info("All events processed.")

if __name__ == "__main__":
    setup_database()
    job()  # Run once at startup
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', hours=24)
    scheduler.start()
    logging.info("Scheduler started. Waiting for next run...")
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down...")
        scheduler.shutdown()
