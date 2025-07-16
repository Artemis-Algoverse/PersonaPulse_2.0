import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_mygov():
    url = "https://www.mygov.in/events/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        print("MyGov response sample:", resp.text[:1000])
        if resp.status_code != 200 or not resp.text:
            logging.warning(f"MyGov: Bad response {resp.status_code}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        events = []
        for card in soup.select(".event-listing, .listing-event"):
            title = card.select_one(".event-title, .title").get_text(strip=True) if card.select_one(".event-title, .title") else None
            link = card.select_one("a[href]")['href'] if card.select_one("a[href]") else None
            date_time = card.select_one(".event-date, .date").get_text(strip=True) if card.select_one(".event-date, .date") else None
            location = card.select_one(".event-location, .location").get_text(strip=True) if card.select_one(".event-location, .location") else "India"
            is_online = "online" in location.lower()
            is_free = True
            is_paid = False
            attending_count = 0
            keywords = title.split() if title else []
            platform = "MyGov"
            try:
                dt = datetime.strptime(date_time, "%d %b %Y") if date_time else None
            except:
                dt = None
            event = {
                "title": title,
                "date_time": dt,
                "location": location,
                "link": link,
                "attending_count": attending_count,
                "is_online": is_online,
                "is_free": is_free,
                "is_paid": is_paid,
                "keywords": keywords,
                "platform": platform,
                "created_at": datetime.now()
            }
            if title and link:
                events.append(event)
        logging.info(f"MyGov: Fetched {len(events)} events.")
        return events
    except Exception as ex:
        logging.error(f"MyGov: Exception {ex}")
        return []
