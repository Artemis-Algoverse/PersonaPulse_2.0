import re
import requests
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import logging

nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words('english'))
DB_PATH = 'events.db'

# Extract keywords from user input or public profile

def extract_keywords_from_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    words = text.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return list(set(keywords))

# Scrape public profile (stub, extend as needed)
def scrape_profile(url):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.text
    except Exception as ex:
        logging.error(f"Error scraping profile: {ex}")
    return ''

# Get all events and their keywords from DB
def get_events_from_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, keywords FROM events")
    events = cur.fetchall()
    conn.close()
    return events

# Match user keywords to event keywords using cosine similarity
def match_user_to_events(user_keywords, top_n=10):
    events = get_events_from_db()
    event_ids = []
    event_titles = []
    event_keywords = []
    for eid, title, kw in events:
        event_ids.append(eid)
        event_titles.append(title)
        event_keywords.append(kw or '')
    # Prepare corpus
    corpus = [' '.join(user_keywords)] + event_keywords
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    scores = [(i, sims[i]) for i in range(len(sims))]
    scores.sort(key=lambda x: x[1], reverse=True)
    top_matches = scores[:top_n]
    result = [{'event_id': event_ids[i], 'title': event_titles[i], 'score': sims[i]} for i, _ in top_matches]
    return result

# Main entry point
def match_user(user_input=None, profile_url=None):
    if profile_url:
        text = scrape_profile(profile_url)
        user_keywords = extract_keywords_from_text(text)
    elif user_input:
        user_keywords = extract_keywords_from_text(user_input)
    else:
        return []
    return match_user_to_events(user_keywords)

## No example usage; only match events when called from backend/frontend
