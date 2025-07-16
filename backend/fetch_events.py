
import logging
from fetch_devpost import fetch_devpost
from fetch_eventbrite import fetch_eventbrite
from fetch_mygov import fetch_mygov
from fetch_ignca import fetch_ignca
from fetch_indiahabitat import fetch_indiahabitat

def fetch_all_events():
    all_events = []
    for fetcher, name in [
        (fetch_devpost, "Devpost"),
        (fetch_eventbrite, "Eventbrite"),
        (fetch_mygov, "MyGov"),
        (fetch_ignca, "IGNCA"),
        (fetch_indiahabitat, "IndiaHabitat")
    ]:
        logging.info(f"Fetching events from {name}...")
        try:
            events = fetcher()
            logging.info(f"Fetched {len(events)} events from {name}.")
            all_events.extend(events)
        except Exception as ex:
            logging.error(f"Error fetching from {name}: {ex}")
    return all_events
