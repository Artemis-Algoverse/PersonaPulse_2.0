import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_devpost():
    url = "https://devpost.com/api/hackathons?challenge_type=all&sort_by=submission_deadline&page=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        print("Devpost API response sample:", resp.text[:1000])
        if resp.status_code != 200 or not resp.text:
            logging.warning(f"Devpost: Bad response {resp.status_code}")
            return []
        data = resp.json()
        events = []
        for hack in data.get('hackathons', []):
            title = hack.get('title')
            link = hack.get('url')
            date_time = hack.get('submission_deadline')
            location = hack.get('location', 'Online')
            is_online = 'online' in location.lower()
            is_free = True
            is_paid = False
            attending_count = hack.get('participants_count', 0)
            keywords = hack.get('tags', [])
            platform = "Devpost"
            try:
                dt = datetime.fromisoformat(date_time) if date_time else None
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
        logging.info(f"Devpost: Fetched {len(events)} events.")
        return events
    except Exception as ex:
        logging.error(f"Devpost: Exception {ex}")
        return []
