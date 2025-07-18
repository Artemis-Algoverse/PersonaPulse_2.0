import sqlite3

# Path to events.db in backend folder
DB_PATH = 'events.db'

# Create table and insert sample events
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    keywords TEXT
)''')

sample_events = [
    ('Tech Innovation Summit', 'A summit for tech enthusiasts and innovators.', 'technology,innovation,networking'),
    ('Startup Mixer', 'Meet and connect with startup founders and investors.', 'startup,networking,business'),
    ('Creative Writing Workshop', 'A workshop for creative writers and storytellers.', 'creative,writing,workshop'),
    ('AI & Data Science Conference', 'Explore the latest in AI and data science.', 'ai,data,science,conference'),
    ('Art & Design Expo', 'Showcase your art and design skills.', 'art,design,expo,creative'),
]

cur.executemany('INSERT INTO events (title, description, keywords) VALUES (?, ?, ?)', sample_events)
conn.commit()
conn.close()
print('Seeded events.db with sample events.')
