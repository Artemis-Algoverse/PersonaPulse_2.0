from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_indiahabitat():
    url = "https://www.indiahabitat.org/events"
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".event-listing, .listing-event")))
        html = driver.page_source
        print("IndiaHabitat response sample:", html[:1000])
        soup = BeautifulSoup(html, "html.parser")
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
            platform = "IndiaHabitat"
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
        logging.info(f"IndiaHabitat: Fetched {len(events)} events.")
        driver.quit()
        return events
    except Exception as ex:
        logging.error(f"IndiaHabitat: Exception {ex}")
        return []
