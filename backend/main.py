import logging
from apscheduler.schedulers.background import BackgroundScheduler
from database import setup_database, insert_events, remove_expired_events
from fetch_events import fetch_all_events
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def run_all_scrapers():
    return fetch_all_events()

def job():
    logging.info("Scheduled job started.")
    remove_expired_events()
    events = run_all_scrapers()
    logging.info(f"Total events fetched: {len(events)}")
    insert_events(events)
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
