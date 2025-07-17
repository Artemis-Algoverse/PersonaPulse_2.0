import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from models import db, UserProfile, ScrapingLog
import logging

logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self):
        self.session = requests.Session()
        # Set user agent to appear as a regular browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_profile(self, twitter_username, unique_persona_pulse_id):
        """Scrape Twitter profile data using web scraping (public data only)"""
        try:
            # Clean username
            username = twitter_username.lstrip('@')
            
            # Try to access public profile through nitter (Twitter proxy) for better access
            # Fallback to direct Twitter if needed
            urls_to_try = [
                f"https://nitter.net/{username}",
                f"https://twitter.com/{username}"
            ]
            
            profile_data = None
            tweets_data = []
            
            for url in urls_to_try:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract profile information
                        if 'nitter.net' in url:
                            profile_data = self._extract_nitter_data(soup, username)
                            tweets_data = self._extract_nitter_tweets(soup)
                        else:
                            profile_data = self._extract_twitter_data(soup, username)
                            tweets_data = self._extract_twitter_tweets(soup)
                        
                        if profile_data:
                            break
                            
                except Exception as e:
                    logger.warning(f"Failed to scrape {url}: {str(e)}")
                    continue
            
            if not profile_data:
                profile_data = {'username': username, 'followers': 0}
            
            # Update database
            user_profile = UserProfile.query.filter_by(unique_persona_pulse_id=unique_persona_pulse_id).first()
            if user_profile:
                user_profile.twitter_id = username
                user_profile.twitter_posts = json.dumps(tweets_data)
                user_profile.twitter_followers_count = profile_data.get('followers', 0)
                user_profile.last_updated = datetime.utcnow()
                
                db.session.commit()
                
                # Log success
                log = ScrapingLog(
                    unique_persona_pulse_id=unique_persona_pulse_id,
                    platform='twitter',
                    status='success' if tweets_data else 'partial',
                    items_scraped=len(tweets_data),
                    error_message='Limited public data available' if not tweets_data else None
                )
                db.session.add(log)
                db.session.commit()
                
                logger.info(f"Successfully scraped Twitter profile: {username}")
                return True
                
        except Exception as e:
            logger.error(f"Error scraping Twitter profile {twitter_username}: {str(e)}")
            
            # Log error
            log = ScrapingLog(
                unique_persona_pulse_id=unique_persona_pulse_id,
                platform='twitter',
                status='failed',
                error_message=str(e),
                items_scraped=0
            )
            db.session.add(log)
            db.session.commit()
            
            return False
    
    def _extract_nitter_data(self, soup, username):
        """Extract profile data from Nitter"""
        try:
            profile_data = {'username': username, 'followers': 0}
            
            # Try to extract follower count
            stats = soup.find_all('span', class_='profile-stat-num')
            if len(stats) >= 2:
                followers_text = stats[1].get_text(strip=True)
                # Convert text like "1.2K" to number
                profile_data['followers'] = self._convert_count_to_number(followers_text)
            
            return profile_data
        except Exception as e:
            logger.warning(f"Error extracting Nitter data: {str(e)}")
            return {'username': username, 'followers': 0}
    
    def _extract_nitter_tweets(self, soup):
        """Extract tweets from Nitter"""
        try:
            tweets = []
            tweet_elements = soup.find_all('div', class_='tweet-content')
            
            for tweet_elem in tweet_elements[:10]:  # Limit to 10 recent tweets
                tweet_text = tweet_elem.get_text(strip=True)
                if tweet_text and len(tweet_text) > 10:  # Filter out very short content
                    tweets.append({
                        'text': tweet_text,
                        'scraped_at': datetime.utcnow().isoformat()
                    })
            
            return tweets
        except Exception as e:
            logger.warning(f"Error extracting Nitter tweets: {str(e)}")
            return []
    
    def _extract_twitter_data(self, soup, username):
        """Extract profile data from Twitter (limited)"""
        try:
            # Twitter's current structure makes it very difficult to scrape without API
            # Return basic structure
            return {'username': username, 'followers': 0}
        except Exception as e:
            logger.warning(f"Error extracting Twitter data: {str(e)}")
            return {'username': username, 'followers': 0}
    
    def _extract_twitter_tweets(self, soup):
        """Extract tweets from Twitter (very limited without API)"""
        try:
            # Twitter heavily restricts web scraping
            # Most content is loaded dynamically via JavaScript
            return []
        except Exception as e:
            logger.warning(f"Error extracting Twitter tweets: {str(e)}")
            return []
    
    def _convert_count_to_number(self, count_text):
        """Convert text like '1.2K' or '500' to number"""
        try:
            count_text = count_text.upper().replace(',', '')
            if 'K' in count_text:
                return int(float(count_text.replace('K', '')) * 1000)
            elif 'M' in count_text:
                return int(float(count_text.replace('M', '')) * 1000000)
            else:
                return int(count_text)
        except:
            return 0
    
    def get_user_tweets_text(self, twitter_username, limit=10):
        """Get text content from recent tweets for AI analysis"""
        try:
            username = twitter_username.lstrip('@')
            
            # Try Nitter first for better access
            url = f"https://nitter.net/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tweets = self._extract_nitter_tweets(soup)
                return [tweet['text'] for tweet in tweets[:limit]]
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting Twitter tweets text: {str(e)}")
            return []
