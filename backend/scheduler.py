from apscheduler.schedulers.background import BackgroundScheduler
from database import remove_expired_events, insert_events
from fetch_events import fetch_all_events
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

scheduler = BackgroundScheduler()

def scheduled_job():
    logging.info('Starting scheduled event scraping job...')
    remove_expired_events()
    all_events = fetch_all_events()
    logging.info(f"Total events scraped: {len(all_events)}")
    insert_events(all_events)
    logging.info('Event scraping job completed.')

def start():
    scheduler.add_job(scheduled_job, 'interval', hours=24, next_run_time=None)
    scheduler.start()
