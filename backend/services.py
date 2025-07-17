import uuid
import logging
from scrapers import InstagramScraper, TwitterScraper, RedditScraper, LinkedInScraper
from ai_analyzer import PersonalityAnalyzer
from models import db, UserProfile, PersonalityData
from config import Config

logger = logging.getLogger(__name__)

class PersonaPulseService:
    def __init__(self):
        # Initialize scrapers (no API credentials needed - web scraping only)
        self.instagram_scraper = InstagramScraper()
        self.twitter_scraper = TwitterScraper()
        self.reddit_scraper = RedditScraper()
        self.linkedin_scraper = LinkedInScraper()
        self.ai_analyzer = PersonalityAnalyzer(Config.GEMINI_API_KEY)
    
    def create_user_profile(self, social_media_ids):
        """Create a new user profile with social media IDs"""
        try:
            # Generate unique ID
            unique_id = str(uuid.uuid4())
            
            # Create user profile
            user_profile = UserProfile(
                unique_persona_pulse_id=unique_id,
                insta_id=social_media_ids.get('instagram'),
                linkedin_id=social_media_ids.get('linkedin'),
                reddit_id=social_media_ids.get('reddit'),
                twitter_id=social_media_ids.get('twitter')
            )
            
            db.session.add(user_profile)
            db.session.commit()
            
            logger.info(f"Created user profile with ID: {unique_id}")
            return unique_id
            
        except Exception as e:
            logger.error(f"Error creating user profile: {str(e)}")
            db.session.rollback()
            return None
    
    def scrape_user_data(self, unique_persona_pulse_id):
        """Scrape social media data for a user"""
        try:
            user_profile = UserProfile.query.filter_by(
                unique_persona_pulse_id=unique_persona_pulse_id
            ).first()
            
            if not user_profile:
                raise Exception(f"User profile not found: {unique_persona_pulse_id}")
            
            scraping_results = {
                'instagram': False,
                'twitter': False,
                'reddit': False,
                'linkedin': False
            }
            
            # Scrape Instagram (public data only)
            if user_profile.insta_id:
                logger.info(f"Scraping Instagram: {user_profile.insta_id}")
                scraping_results['instagram'] = self.instagram_scraper.scrape_profile(
                    user_profile.insta_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape Twitter
            if user_profile.twitter_id:
                logger.info(f"Scraping Twitter: {user_profile.twitter_id}")
                scraping_results['twitter'] = self.twitter_scraper.scrape_profile(
                    user_profile.twitter_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape Reddit
            if user_profile.reddit_id:
                logger.info(f"Scraping Reddit: {user_profile.reddit_id}")
                scraping_results['reddit'] = self.reddit_scraper.scrape_profile(
                    user_profile.reddit_id, 
                    unique_persona_pulse_id
                )
            
            # Scrape LinkedIn
            if user_profile.linkedin_id:
                logger.info(f"Scraping LinkedIn: {user_profile.linkedin_id}")
                scraping_results['linkedin'] = self.linkedin_scraper.scrape_profile(
                    user_profile.linkedin_id, 
                    unique_persona_pulse_id
                )
            
            logger.info(f"Scraping completed for user: {unique_persona_pulse_id}")
            return scraping_results
            
        except Exception as e:
            logger.error(f"Error scraping user data: {str(e)}")
            return None
        finally:
            # Close LinkedIn scraper
            self.linkedin_scraper.close()
    
    def analyze_user_personality(self, unique_persona_pulse_id):
        """Analyze user personality using AI"""
        try:
            logger.info(f"Analyzing personality for user: {unique_persona_pulse_id}")
            analysis_result = self.ai_analyzer.analyze_personality(unique_persona_pulse_id)
            
            if analysis_result:
                logger.info(f"Personality analysis completed for user: {unique_persona_pulse_id}")
                return analysis_result
            else:
                logger.error(f"Personality analysis failed for user: {unique_persona_pulse_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing personality: {str(e)}")
            return None
    
    def process_new_user(self, social_media_ids):
        """Complete pipeline: create user, scrape data, analyze personality"""
        try:
            # Step 1: Create user profile
            unique_id = self.create_user_profile(social_media_ids)
            if not unique_id:
                return None
            
            # Step 2: Scrape social media data
            scraping_results = self.scrape_user_data(unique_id)
            if not scraping_results:
                logger.error(f"Failed to scrape data for user: {unique_id}")
                return None
            
            # Step 3: Analyze personality
            analysis_result = self.analyze_user_personality(unique_id)
            if not analysis_result:
                logger.error(f"Failed to analyze personality for user: {unique_id}")
                return None
            
            return {
                'unique_persona_pulse_id': unique_id,
                'scraping_results': scraping_results,
                'personality_analysis': analysis_result
            }
            
        except Exception as e:
            logger.error(f"Error processing new user: {str(e)}")
            return None
    
    def get_user_profile(self, unique_persona_pulse_id):
        """Get complete user profile with personality data"""
        try:
            user_profile = UserProfile.query.filter_by(
                unique_persona_pulse_id=unique_persona_pulse_id
            ).first()
            
            if not user_profile:
                return None
            
            personality_data = PersonalityData.query.filter_by(
                unique_persona_pulse_id=unique_persona_pulse_id
            ).first()
            
            result = user_profile.to_dict()
            if personality_data:
                result['personality_data'] = personality_data.to_dict()
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None
    
    def get_all_users(self):
        """Get all user profiles"""
        try:
            users = UserProfile.query.all()
            result = []
            
            for user in users:
                user_data = user.to_dict()
                personality_data = PersonalityData.query.filter_by(
                    unique_persona_pulse_id=user.unique_persona_pulse_id
                ).first()
                
                if personality_data:
                    user_data['personality_data'] = personality_data.to_dict()
                
                result.append(user_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []
