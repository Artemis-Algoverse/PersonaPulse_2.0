
import logging

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import logging

def fetch_meraevents():
    print("📡 Fetching events from MeraEvents...")
    events = []
    url = "https://www.meraevents.com/events/delhi"
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ])
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Response status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            event_cards = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|listing', re.I))[:20]
            print(f"   Found {len(event_cards)} potential event cards")
            for card in event_cards:
                title_elem = (
                    card.find(['h1', 'h2', 'h3', 'h4']) or
                    card.find(['span', 'div'], class_=re.compile(r'title|name')) or
                    card.find('a', href=True)
                )
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if len(title) > 5:
                        link_elem = card.find('a', href=True)
                        link = url
                        if link_elem and link_elem['href']:
                            link = link_elem['href']
                            if not link.startswith("http"):
                                link = "https://www.meraevents.com" + link
                        date_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'date|event-date|event-time|start-date|start-time|date-time', re.I))
                        date_time = date_elem.get_text(strip=True) if date_elem else None
                        location_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'location|venue|place', re.I))
                        location = location_elem.get_text(strip=True) if location_elem else "Delhi"
                        is_online = "online" in location.lower()
                        event = {
                            'title': title,
                            'date_time': date_time,
                            'location': location,
                            'description': f'MeraEvents event: {title}',
                            'link': link,
                            'attending_count': 0,
                            'is_online': is_online,
                            'is_free': True,
                            'is_paid': False,
                            'keywords': ["meraevents", "delhi"],
                            'platform': 'MeraEvents',
                            'created_at': datetime.now()
                        }
                        events.append(event)
            print(f"✅ Found {len(events)} events from MeraEvents.")
        time.sleep(random.uniform(1, 2))
    except Exception as e:
        print(f"❌ Error fetching MeraEvents: {str(e)}")
    return events
