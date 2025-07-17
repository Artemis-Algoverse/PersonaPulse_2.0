import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, 'instance', 'personapulse.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # AI API Key (only external API needed)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Scheduler
    SCHEDULER_INTERVAL_HOURS = 24
    
    # Note: All social media data collection is done through web scraping
    # using usernames provided via the web form. No API keys required.
