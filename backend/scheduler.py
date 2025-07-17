from apscheduler.schedulers.background import BackgroundScheduler
<<<<<<< HEAD
from apscheduler.triggers.interval import IntervalTrigger
from scrapers import InstagramScraper, TwitterScraper, RedditScraper, LinkedInScraper
from ai_analyzer import PersonalityAnalyzer
from models import db, UserProfile
from config import Config
import logging
import atexit

logger = logging.getLogger(__name__)

class DataScheduler:
    def __init__(self, app):
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        # Shutdown scheduler when app exits
        atexit.register(lambda: self.scheduler.shutdown())
        
        # Initialize scrapers (no API credentials needed - web scraping only)
        self.instagram_scraper = InstagramScraper()
        self.twitter_scraper = TwitterScraper()
        self.reddit_scraper = RedditScraper()
        self.linkedin_scraper = LinkedInScraper()
        self.ai_analyzer = PersonalityAnalyzer(Config.GEMINI_API_KEY)
    
    def schedule_daily_update(self):
        """Schedule daily data update job"""
        self.scheduler.add_job(
            func=self.update_all_user_data,
            trigger=IntervalTrigger(hours=Config.SCHEDULER_INTERVAL_HOURS),
            id='daily_update_job',
            name='Update all user social media data',
            replace_existing=True
        )
        logger.info(f"Scheduled daily update job every {Config.SCHEDULER_INTERVAL_HOURS} hours")
    
    def update_all_user_data(self):
        """Update social media data for all users"""
        with self.app.app_context():
            try:
                users = UserProfile.query.all()
                logger.info(f"Starting scheduled update for {len(users)} users")
                
                for user in users:
                    self.update_user_data(user.unique_persona_pulse_id)
                
                logger.info("Completed scheduled update for all users")
                
            except Exception as e:
                logger.error(f"Error in scheduled update: {str(e)}")
    
    def update_user_data(self, unique_persona_pulse_id):
        """Update social media data for a specific user"""
        try:
            user_profile = UserProfile.query.filter_by(
                unique_persona_pulse_id=unique_persona_pulse_id
            ).first()
            
            if not user_profile:
                logger.warning(f"User profile not found: {unique_persona_pulse_id}")
                return
            
            # Scrape Instagram (public data only)
            if user_profile.insta_id:
                logger.info(f"Updating Instagram data for user: {unique_persona_pulse_id}")
                self.instagram_scraper.scrape_profile(
                    user_profile.insta_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape Twitter
            if user_profile.twitter_id:
                logger.info(f"Updating Twitter data for user: {unique_persona_pulse_id}")
                self.twitter_scraper.scrape_profile(
                    user_profile.twitter_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape Reddit
            if user_profile.reddit_id:
                logger.info(f"Updating Reddit data for user: {unique_persona_pulse_id}")
                self.reddit_scraper.scrape_profile(
                    user_profile.reddit_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape LinkedIn
            if user_profile.linkedin_id:
                logger.info(f"Updating LinkedIn data for user: {unique_persona_pulse_id}")
                self.linkedin_scraper.scrape_profile(
                    user_profile.linkedin_id, 
                    unique_persona_pulse_id
                )
            
            # Analyze personality with updated data
            logger.info(f"Analyzing personality for user: {unique_persona_pulse_id}")
            self.ai_analyzer.analyze_personality(unique_persona_pulse_id)
            
            logger.info(f"Successfully updated data for user: {unique_persona_pulse_id}")
            
        except Exception as e:
            logger.error(f"Error updating user data for {unique_persona_pulse_id}: {str(e)}")
        finally:
            # Close LinkedIn scraper
            self.linkedin_scraper.close()
    
    def manual_update_user(self, unique_persona_pulse_id):
        """Manually trigger update for a specific user"""
        logger.info(f"Manual update triggered for user: {unique_persona_pulse_id}")
        self.update_user_data(unique_persona_pulse_id)
    
    def get_job_status(self):
        """Get status of scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        job_info = []
        
        for job in jobs:
            job_info.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return job_info
=======
from database import remove_expired_events, insert_events
from fetch_events import fetch_all_events
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

scheduler = BackgroundScheduler()

def scheduled_job():
    logging.info('Starting scheduled event scraping job...')
    remove_expired_events()
    all_events = fetch_all_events()
    logging.info(f"Total events scraped: {len(all_events)}")
    insert_events(all_events)
    logging.info('Event scraping job completed.')

def start():
    scheduler.add_job(scheduled_job, 'interval', hours=24, next_run_time=None)
    scheduler.start()
>>>>>>> 45b4459130aba403532d1b74a1ae2367f6d07130
