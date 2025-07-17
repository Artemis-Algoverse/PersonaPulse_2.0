import asyncio
from playwright.async_api import async_playwright
import logging

async def fetch_events_from_eventbrite():
    url = "https://www.eventbrite.com/d/india--delhi/events/"
    events = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_selector('.eds-event-card-content__content', timeout=20000)
            cards = await page.query_selector_all('.eds-event-card-content__content')
            for card in cards:
                title = await card.query_selector_eval('.eds-event-card-content__title', 'el => el.textContent', timeout=5000) if await card.query_selector('.eds-event-card-content__title') else None
                date_time = await card.query_selector_eval('.eds-text-bs--fixed', 'el => el.textContent', timeout=5000) if await card.query_selector('.eds-text-bs--fixed') else None
                location = await card.query_selector_eval('.card-text--truncated__one-line', 'el => el.textContent', timeout=5000) if await card.query_selector('.card-text--truncated__one-line') else "India"
                link_tag = await card.query_selector('a[href]')
                link = await link_tag.get_attribute('href') if link_tag else None
                img_tag = await card.query_selector('img')
                image_url = await img_tag.get_attribute('src') if img_tag else None
                event = {
                    "title": title.strip() if title else None,
                    "date": date_time.strip() if date_time else None,
                    "location": location.strip() if location else None,
                    "link": link,
                    "image_url": image_url
                }
                if event["title"] and event["link"]:
                    events.append(event)
        except Exception as ex:
            logging.error(f"Eventbrite Playwright: Exception {ex}")
        await context.close()
        await browser.close()
    return events

# Repeat similar for other platforms
async def fetch_events_from_meraevents():
    url = "https://www.meraevents.com/events/delhi"
    events = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_selector('.eventBlock, .event-listing, .event-card', timeout=20000)
            cards = await page.query_selector_all('.eventBlock, .event-listing, .event-card')
            for card in cards:
                title = await card.query_selector_eval('.eventTitle, .event-title, .title', 'el => el.textContent', timeout=5000) if await card.query_selector('.eventTitle, .event-title, .title') else None
                date_time = await card.query_selector_eval('.eventDate, .date', 'el => el.textContent', timeout=5000) if await card.query_selector('.eventDate, .date') else None
                location = await card.query_selector_eval('.eventLocation, .location, .venue', 'el => el.textContent', timeout=5000) if await card.query_selector('.eventLocation, .location, .venue') else "Delhi"
                link_tag = await card.query_selector('a[href]')
                link = await link_tag.get_attribute('href') if link_tag else None
                img_tag = await card.query_selector('img')
                image_url = await img_tag.get_attribute('src') if img_tag else None
                event = {
                    "title": title.strip() if title else None,
                    "date": date_time.strip() if date_time else None,
                    "location": location.strip() if location else None,
                    "link": link,
                    "image_url": image_url
                }
                if event["title"] and event["link"]:
                    events.append(event)
        except Exception as ex:
            logging.error(f"MeraEvents Playwright: Exception {ex}")
        await context.close()
        await browser.close()
    return events

# You can add similar async functions for BookMyShow, Townscript, AllEvents

async def fetch_all_playwright_events():
    results = await asyncio.gather(
        fetch_events_from_eventbrite(),
        fetch_events_from_meraevents(),
        # Add other fetchers here
    )
    all_events = []
    for site_events in results:
        all_events.extend(site_events)
    return all_events

# Example usage:
# asyncio.run(fetch_all_playwright_events())
