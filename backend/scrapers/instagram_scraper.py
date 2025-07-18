import instaloader
import json
import time
from datetime import datetime
from models import db, UserProfile, ScrapingLog
import logging

logger = logging.getLogger(__name__)

class InstagramScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        # Configure for anonymous access to public data
        self.loader.context.log = lambda *args, **kwargs: None  # Disable logging
        
    def scrape_profile(self, instagram_username, unique_persona_pulse_id):
        """Scrape Instagram profile data (public data only)"""
        bio = ''
        hashtags = set()
        followers = 0
        following = 0
        posts_data = []
        try:
            # Try to get profile (public data only)
            try:
                profile = instaloader.Profile.from_username(self.loader.context, instagram_username)
                bio = profile.biography
                followers = profile.followers
                following = profile.followees
                post_count = 0
                for post in profile.get_posts():
                    if post_count >= 20:
                        break
                    if post.caption:
                        post_info = {
                            'caption': post.caption,
                            'likes': post.likes,
                            'comments': post.comments,
                            'date': post.date.isoformat(),
                            'hashtags': post.caption_hashtags if post.caption_hashtags else []
                        }
                        posts_data.append(post_info)
                        if post.caption_hashtags:
                            hashtags.update(post.caption_hashtags)
                    post_count += 1
                    time.sleep(2)
            except Exception as e:
                logger.warning(f"Could not access Instagram API for {instagram_username}: {str(e)}")
                # Try fallback scraping or leave bio empty
            # Update database
            user_profile = UserProfile.query.filter_by(unique_persona_pulse_id=unique_persona_pulse_id).first()
            if user_profile:
                user_profile.insta_id = instagram_username
                user_profile.insta_bio = bio
                user_profile.insta_posts_hashtags = json.dumps(list(hashtags))
                user_profile.insta_followers_count = followers
                user_profile.insta_following_count = following
                user_profile.last_updated = datetime.utcnow()
                db.session.commit()
                log = ScrapingLog(
                    unique_persona_pulse_id=unique_persona_pulse_id,
                    platform='instagram',
                    status='success' if bio else 'partial',
                    items_scraped=len(posts_data)
                )
                db.session.add(log)
                db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error scraping Instagram profile {instagram_username}: {str(e)}")
            return False
                
            # logger.info(f"Successfully scraped Instagram profile: {instagram_username}")
            return True
                
        except Exception as e:
            logger.error(f"Error scraping Instagram profile {instagram_username}: {str(e)}")
            
            # Log error
            log = ScrapingLog(
                unique_persona_pulse_id=unique_persona_pulse_id,
                platform='instagram',
                status='failed',
                error_message=str(e),
                items_scraped=0
            )
            db.session.add(log)
            db.session.commit()
            
            return False
    
    def get_profile_posts_text(self, instagram_username, limit=20):
        """Get text content from recent public posts for AI analysis"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, instagram_username)
            
            posts_text = []
            post_count = 0
            
            for post in profile.get_posts():
                if post_count >= limit:
                    break
                
                if post.caption:
                    posts_text.append(post.caption)
                
                post_count += 1
                time.sleep(2)  # Rate limiting
            
            return posts_text
            
        except Exception as e:
            logger.error(f"Error getting Instagram posts text: {str(e)}")
            return []
