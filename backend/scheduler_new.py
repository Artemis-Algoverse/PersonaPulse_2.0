from apscheduler.schedulers.background import BackgroundScheduler
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
        self.analyzer = PersonalityAnalyzer()
        
        # Initialize scrapers
        self.scrapers = {
            'instagram': InstagramScraper(),
            'twitter': TwitterScraper(),
            'reddit': RedditScraper(),
            'linkedin': LinkedInScraper()
        }
        
        # Ensure scheduler shuts down properly
        atexit.register(lambda: self.scheduler.shutdown())
    
    def schedule_daily_update(self):
        """Schedule daily updates for all users"""
        try:
            if self.scheduler.running:
                logger.info("Scheduler already running")
                return
                
            # Add job for daily updates
            self.scheduler.add_job(
                func=self.daily_update_job,
                trigger=IntervalTrigger(hours=Config.SCHEDULER_INTERVAL_HOURS),
                id='daily_update',
                name='Daily User Data Update',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info(f"Scheduled daily updates every {Config.SCHEDULER_INTERVAL_HOURS} hours")
            
        except Exception as e:
            logger.error(f"Error scheduling daily updates: {str(e)}")
    
    def daily_update_job(self):
        """Job to update all users' data"""
        with self.app.app_context():
            try:
                logger.info("Starting daily update job")
                
                # Get all users
                users = UserProfile.query.all()
                logger.info(f"Found {len(users)} users to update")
                
                for user in users:
                    try:
                        # Update user data
                        self.update_user_data(user.unique_persona_pulse_id)
                        
                    except Exception as e:
                        logger.error(f"Error updating user {user.unique_persona_pulse_id}: {str(e)}")
                        continue
                
                logger.info("Daily update job completed")
                
            except Exception as e:
                logger.error(f"Error in daily update job: {str(e)}")
    
    def update_user_data(self, unique_id):
        """Update data for a specific user"""
        try:
            user = UserProfile.query.filter_by(unique_persona_pulse_id=unique_id).first()
            if not user:
                logger.warning(f"User {unique_id} not found")
                return False
            
            # Scrape fresh data
            scraping_results = {}
            social_media_ids = user.social_media_ids
            
            for platform, username in social_media_ids.items():
                if platform in self.scrapers and username:
                    try:
                        scraper = self.scrapers[platform]
                        data = scraper.scrape_user_data(username)
                        scraping_results[platform] = bool(data)
                        
                        # Update user's scraped data
                        if data:
                            setattr(user, f'{platform}_data', data)
                            
                    except Exception as e:
                        logger.error(f"Error scraping {platform} for {username}: {str(e)}")
                        scraping_results[platform] = False
            
            # Update personality analysis
            try:
                personality_data = self.analyzer.analyze_personality(user)
                if personality_data:
                    # Update or create personality data
                    if user.personality_data:
                        for key, value in personality_data.items():
                            setattr(user.personality_data, key, value)
                    else:
                        from models import PersonalityData
                        new_personality = PersonalityData(
                            user_id=user.id,
                            **personality_data
                        )
                        db.session.add(new_personality)
                        
            except Exception as e:
                logger.error(f"Error analyzing personality for {unique_id}: {str(e)}")
            
            # Save changes
            db.session.commit()
            logger.info(f"Updated data for user {unique_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating user data for {unique_id}: {str(e)}")
            db.session.rollback()
            return False
    
    def get_job_status(self):
        """Get status of scheduled jobs"""
        jobs = []
        
        if self.scheduler.running:
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
        
        return {
            'scheduler_running': self.scheduler.running,
            'jobs': jobs,
            'interval_hours': Config.SCHEDULER_INTERVAL_HOURS
        }
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def start_scheduler(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
