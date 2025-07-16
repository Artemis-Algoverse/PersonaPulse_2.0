import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_devpost():
    url = "https://devpost.com/hackathons?search=india"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        print("Devpost response sample:", resp.text[:1000])
        if resp.status_code != 200 or not resp.text:
            logging.warning(f"Devpost: Bad response {resp.status_code}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        events = []
        for card in soup.select(".challenge-card-wrapper, .hackathon-card"):
            title = card.select_one(".challenge-title, .title").get_text(strip=True) if card.select_one(".challenge-title, .title") else None
            link = card.select_one("a[href]")['href'] if card.select_one("a[href]") else None
            if link and not link.startswith("http"):
                link = "https://devpost.com" + link
            date_time = card.select_one(".challenge-date, .date").get_text(strip=True) if card.select_one(".challenge-date, .date") else None
            location = card.select_one(".challenge-location, .location").get_text(strip=True) if card.select_one(".challenge-location, .location") else "Online"
            is_online = "online" in location.lower()
            is_free = True
            is_paid = False
            attending_count = 0
            keywords = title.split() if title else []
            platform = "Devpost"
            try:
                dt = datetime.strptime(date_time, "%b %d, %Y") if date_time else None
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
