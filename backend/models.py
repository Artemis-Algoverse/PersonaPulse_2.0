from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class UserProfile(db.Model):
    """Raw data scraped from social media platforms"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_persona_pulse_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # Social Media IDs
    insta_id = db.Column(db.String(100), nullable=True)
    linkedin_id = db.Column(db.String(100), nullable=True)
    reddit_id = db.Column(db.String(100), nullable=True)
    twitter_id = db.Column(db.String(100), nullable=True)
    
    # Profile Information
    insta_bio = db.Column(db.Text, nullable=True)
    linkedin_about = db.Column(db.Text, nullable=True)
    
    # Posts and Content
    insta_posts_hashtags = db.Column(db.Text, nullable=True)  # JSON string
    reddit_posts = db.Column(db.Text, nullable=True)  # JSON string
    twitter_posts = db.Column(db.Text, nullable=True)  # JSON string
    
    # Additional scraped data
    insta_followers_count = db.Column(db.Integer, nullable=True)
    insta_following_count = db.Column(db.Integer, nullable=True)
    linkedin_connections = db.Column(db.Integer, nullable=True)
    reddit_karma = db.Column(db.Integer, nullable=True)
    twitter_followers_count = db.Column(db.Integer, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    personality_data = db.relationship('PersonalityData', backref='user_profile', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'unique_persona_pulse_id': self.unique_persona_pulse_id,
            'insta_id': self.insta_id,
            'linkedin_id': self.linkedin_id,
            'reddit_id': self.reddit_id,
            'twitter_id': self.twitter_id,
            'insta_bio': self.insta_bio,
            'linkedin_about': self.linkedin_about,
            'insta_posts_hashtags': json.loads(self.insta_posts_hashtags) if self.insta_posts_hashtags else [],
            'reddit_posts': json.loads(self.reddit_posts) if self.reddit_posts else [],
            'twitter_posts': json.loads(self.twitter_posts) if self.twitter_posts else [],
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }

class PersonalityData(db.Model):
    """Processed personality data from GenAI analysis"""
    __tablename__ = 'personality_data'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_persona_pulse_id = db.Column(db.String(100), db.ForeignKey('user_profiles.unique_persona_pulse_id'), unique=True, nullable=False)
    
    # Interest keywords (JSON string)
    list_of_interest_keywords = db.Column(db.Text, nullable=False)  # JSON array
    
    # OCEAN personality traits (0-100 scale)
    openness = db.Column(db.Float, nullable=False)
    conscientiousness = db.Column(db.Float, nullable=False)
    extraversion = db.Column(db.Float, nullable=False)
    agreeableness = db.Column(db.Float, nullable=False)
    neuroticism = db.Column(db.Float, nullable=False)
    
    # Additional analysis
    confidence_score = db.Column(db.Float, nullable=True)  # Confidence in the analysis
    dominant_traits = db.Column(db.String(500), nullable=True)  # Top personality traits
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'unique_persona_pulse_id': self.unique_persona_pulse_id,
            'list_of_interest_keywords': json.loads(self.list_of_interest_keywords),
            'ocean_ranking': {
                'openness': self.openness,
                'conscientiousness': self.conscientiousness,
                'extraversion': self.extraversion,
                'agreeableness': self.agreeableness,
                'neuroticism': self.neuroticism
            },
            'confidence_score': self.confidence_score,
            'dominant_traits': self.dominant_traits,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat()
        }

class ScrapingLog(db.Model):
    """Log of scraping activities"""
    __tablename__ = 'scraping_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_persona_pulse_id = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # instagram, linkedin, reddit, twitter
    status = db.Column(db.String(20), nullable=False)  # success, failed, partial
    error_message = db.Column(db.Text, nullable=True)
    items_scraped = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'unique_persona_pulse_id': self.unique_persona_pulse_id,
            'platform': self.platform,
            'status': self.status,
            'error_message': self.error_message,
            'items_scraped': self.items_scraped,
            'timestamp': self.timestamp.isoformat()
        }
