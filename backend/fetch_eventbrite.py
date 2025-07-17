
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
import logging

def fetch_eventbrite():
    print("📡 Fetching events from Eventbrite...")
    events = []
    search_terms = [
        'tech', 'programming', 'coding', 'software', 'ai', 'machine-learning', 
        'data-science', 'web-development', 'blockchain', 'cybersecurity',
        'startup', 'business', 'entrepreneurship', 'networking', 'marketing', 
        'finance', 'investment', 'leadership',
        'workshop', 'seminar', 'training', 'conference', 'education', 'certification',
        'health', 'fitness', 'wellness', 'yoga', 'meditation', 'nutrition', 
        'mental-health', 'mindfulness',
        'art', 'music', 'photography', 'design', 'creative', 'writing', 
        'dance', 'film',
        'cooking', 'food', 'travel', 'language', 'gaming', 'sports', 
        'community', 'volunteer',
        'science', 'research', 'innovation', 'environment'
    ]
    print(f"🔍 Searching with {len(search_terms)} different terms...")
    print(f"🎯 Target: 1 event per search term = {len(search_terms)} total events")
    for term in search_terms:
        print(f"\n🌐 Searching Eventbrite for: '{term}'")
        eventbrite_url = f"https://www.eventbrite.com/d/online/{term}--events/"
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
            ])
        }
        try:
            response = requests.get(eventbrite_url, headers=headers, timeout=10)
            print(f"📊 Response status: {response.status_code}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                event_cards = (
                    soup.find_all(['div', 'article'], class_=re.compile(r'event|card'))[:10] or
                    soup.find_all(['div', 'article'], attrs={'data-event-id': True})[:10] or
                    soup.find_all(['a'], href=re.compile(r'/e/'))[:10]
                )
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
                            if not any(event['title'].lower() == title.lower() for event in events):
                                link_elem = card.find('a', href=True)
                                event_url = eventbrite_url
                                if link_elem and '/e/' in link_elem['href']:
                                    event_url = 'https://eventbrite.com' + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href']
                                event_date = ''
                                time_elem = card.find('time', attrs={'datetime': True})
                                if time_elem:
                                    datetime_attr = time_elem.get('datetime')
                                    if datetime_attr:
                                        try:
                                            parsed_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                                            event_date = parsed_date.strftime('%a, %b %d, %I:%M %p %Z')
                                        except:
                                            pass
                                if not event_date:
                                    card_text = card.get_text()
                                    date_patterns = [
                                        r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}[\s,]*\d{1,2}:\d{2}\s*(AM|PM|am|pm)?\s*(CDT|CST|EST|PST|GMT|UTC|[A-Z]{3})?',
                                        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}[\s,]*\d{1,2}:\d{2}\s*(AM|PM|am|pm)?\s*(CDT|CST|EST|PST|GMT|UTC|[A-Z]{3})?',
                                        r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}',
                                        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}',
                                        r'\d{1,2}/\d{1,2}/\d{2,4}\s*[\s,]*\d{1,2}:\d{2}\s*(AM|PM|am|pm)?',
                                        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}',
                                        r'\d{1,2}/\d{1,2}/\d{2,4}'
                                    ]
                                    for pattern in date_patterns:
                                        date_matches = re.findall(pattern, card_text, re.I)
                                        if date_matches:
                                            candidate_date = date_matches[0]
                                            if isinstance(candidate_date, tuple):
                                                candidate_date = ' '.join(candidate_date)
                                            if not any(unwanted in candidate_date.lower() for unwanted in [
                                                'save this event', 'add to calendar', 'register', 'buy tickets',
                                                'today', 'tomorrow', 'this week', 'next week', 'soon', 'tbd',
                                                'follow', 'share', 'like', 'comment'
                                            ]):
                                                clean_date = re.sub(r'\s+', ' ', candidate_date.strip())
                                                clean_date = re.sub(r'[^\w\s,/:-]', '', clean_date)
                                                if len(clean_date) > 5:
                                                    event_date = clean_date[:80]
                                                    break
                                if not event_date:
                                    date_selectors = [
                                        card.find(['span', 'div'], class_=re.compile(r'event-date|event-time|start-date|start-time|date-time', re.I)),
                                        card.find(['span', 'div'], attrs={'data-automation': re.compile(r'event-date|event-time|start-date')}),
                                        card.find('time'),
                                        card.find(['span', 'div', 'p'], string=re.compile(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)', re.I)),
                                        card.find(['span', 'div', 'p'], string=re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', re.I))
                                    ]
                                    for date_elem in date_selectors:
                                        if date_elem:
                                            date_text = date_elem.get_text(strip=True)
                                            if date_text and len(date_text) > 5:
                                                if (any(month in date_text.lower() for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']) or 
                                                    re.search(r'\d{1,2}/\d{1,2}', date_text) or
                                                    re.search(r'\d{4}-\d{2}-\d{2}', date_text) or
                                                    re.search(r'\d{1,2}:\d{2}', date_text)):
                                                    if not any(unwanted in date_text.lower() for unwanted in [
                                                        'save this event', 'add to calendar', 'register', 'buy tickets',
                                                        'today', 'tomorrow', 'this week', 'next week', 'soon', 'tbd',
                                                        'follow', 'share', 'like', 'comment', 'view details'
                                                    ]):
                                                        clean_date = re.sub(r'[^\w\s,/:-]', ' ', date_text)
                                                        clean_date = re.sub(r'\s+', ' ', clean_date.strip())
                                                        if len(clean_date) > 5:
                                                            event_date = clean_date[:60]
                                                            break
                                if not event_date and link_elem and '/e/' in link_elem['href']:
                                    try:
                                        event_page_url = 'https://eventbrite.com' + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href']
                                        print(f"🔍 Fetching date from event page: {title[:30]}...")
                                        page_response = requests.get(event_page_url, headers=headers, timeout=8)
                                        if page_response.status_code == 200:
                                            page_soup = BeautifulSoup(page_response.content, 'html.parser')
                                            page_time_elem = page_soup.find('time', attrs={'datetime': True})
                                            if page_time_elem:
                                                datetime_attr = page_time_elem.get('datetime')
                                                if datetime_attr:
                                                    try:
                                                        parsed_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                                                        event_date = parsed_date.strftime('%a, %b %d, %I:%M %p %Z')
                                                    except:
                                                        pass
                                            if not event_date:
                                                page_text = page_soup.get_text()
                                                date_match = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}[\s,]*\d{1,2}:\d{2}\s*(AM|PM|am|pm)?\s*(CDT|CST|EST|PST|GMT|UTC|[A-Z]{3})?', page_text, re.I)
                                                if date_match:
                                                    event_date = date_match.group(0).strip()
                                        time.sleep(0.5)
                                    except:
                                        pass
                                events.append({
                                    'title': title,
                                    'date_time': event_date,
                                    'location': 'Online',
                                    'description': f'{term.title()} event: {title}',
                                    'link': event_url,
                                    'attending_count': 0,
                                    'is_online': True,
                                    'is_free': True,
                                    'is_paid': False,
                                    'keywords': [term, 'online', 'eventbrite'],
                                    'platform': 'Eventbrite',
                                    'created_at': datetime.now()
                                })
                                print(f"✅ Found event for '{term}': {title[:50]}...")
                                break
                time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"❌ Error searching '{term}': {str(e)}")
            continue
    print(f"\n📊 Total events found from Eventbrite: {len(events)}")
    return events
