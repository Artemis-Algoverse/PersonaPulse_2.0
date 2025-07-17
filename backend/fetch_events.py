
import logging
import asyncio
from fetch_devpost import fetch_devpost
from fetch_eventbrite import fetch_eventbrite
from fetch_meraevents import fetch_meraevents

async def fetch_all_events_async():
    all_events = []
    fetchers = [
        (fetch_devpost, "Devpost", False),
        (fetch_eventbrite, "Eventbrite", True),
        (fetch_meraevents, "MeraEvents", True)
    ]
    tasks = []
    for fetcher, name, is_async in fetchers:
        logging.info(f"Fetching events from {name}...")
        if is_async:
            tasks.append(fetcher())
        else:
            # Wrap sync fetcher for asyncio
            loop = asyncio.get_event_loop()
            tasks.append(loop.run_in_executor(None, fetcher))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for idx, (fetcher, name, _) in enumerate(fetchers):
        events = results[idx]
        if isinstance(events, Exception):
            logging.error(f"Error fetching from {name}: {events}")
        else:
            logging.info(f"Fetched {len(events)} events from {name}.")
            all_events.extend(events)
    return all_events
