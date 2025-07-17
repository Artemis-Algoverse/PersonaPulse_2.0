import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from models import db, UserProfile, ScrapingLog
import logging

logger = logging.getLogger(__name__)

class RedditScraper:
    def __init__(self):
        self.session = requests.Session()
        # Set user agent to appear as a regular browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_profile(self, reddit_username, unique_persona_pulse_id):
        """Scrape Reddit profile data using web scraping (public data only)"""
        try:
            # Clean username
            username = reddit_username.lstrip('u/')
            if username.startswith('/'):
                username = username[1:]
            
            # Reddit URLs to try
            urls_to_try = [
                f"https://old.reddit.com/user/{username}",
                f"https://www.reddit.com/user/{username}"
            ]
            
            profile_data = None
            posts_data = []
            comments_data = []
            
            for url in urls_to_try:
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        if 'old.reddit.com' in url:
                            profile_data, posts_data, comments_data = self._extract_old_reddit_data(soup, username)
                        else:
                            profile_data, posts_data, comments_data = self._extract_reddit_data(soup, username)
                        
                        if profile_data:
                            break
                            
                except Exception as e:
                    logger.warning(f"Failed to scrape {url}: {str(e)}")
                    continue
            
            if not profile_data:
                profile_data = {'username': username, 'karma': 0}
            
            # Combine posts and comments for storage
            all_content = posts_data + comments_data
            
            # Update database
            user_profile = UserProfile.query.filter_by(unique_persona_pulse_id=unique_persona_pulse_id).first()
            if user_profile:
                user_profile.reddit_id = username
                user_profile.reddit_posts = json.dumps(all_content)
                user_profile.reddit_karma = profile_data.get('karma', 0)
                user_profile.last_updated = datetime.utcnow()
                
                db.session.commit()
                
                # Log success
                log = ScrapingLog(
                    unique_persona_pulse_id=unique_persona_pulse_id,
                    platform='reddit',
                    status='success' if all_content else 'partial',
                    items_scraped=len(all_content),
                    error_message='Limited public data available' if not all_content else None
                )
                db.session.add(log)
                db.session.commit()
                
                logger.info(f"Successfully scraped Reddit profile: {username}")
                return True
                
        except Exception as e:
            logger.error(f"Error scraping Reddit profile {reddit_username}: {str(e)}")
            
            # Log error
            log = ScrapingLog(
                unique_persona_pulse_id=unique_persona_pulse_id,
                platform='reddit',
                status='failed',
                error_message=str(e),
                items_scraped=0
            )
            db.session.add(log)
            db.session.commit()
            
            return False
    
    def _extract_old_reddit_data(self, soup, username):
        """Extract profile data from old.reddit.com"""
        try:
            profile_data = {'username': username, 'karma': 0}
            posts_data = []
            comments_data = []
            
            # Try to extract karma
            karma_elements = soup.find_all('span', class_='karma')
            if karma_elements:
                for karma_elem in karma_elements:
                    karma_text = karma_elem.get_text(strip=True)
                    karma_match = re.search(r'(\d+)', karma_text)
                    if karma_match:
                        profile_data['karma'] = int(karma_match.group(1))
                        break
            
            # Extract posts and comments
            content_elements = soup.find_all('div', class_='entry')
            
            for content_elem in content_elements[:20]:  # Limit to recent content
                try:
                    # Check if it's a post or comment
                    title_elem = content_elem.find('a', class_='title')
                    
                    if title_elem:  # It's a post
                        post_text = title_elem.get_text(strip=True)
                        # Try to get post body if available
                        body_elem = content_elem.find('div', class_='usertext-body')
                        if body_elem:
                            body_text = body_elem.get_text(strip=True)
                            post_text += " " + body_text
                        
                        if post_text and len(post_text) > 10:
                            posts_data.append({
                                'type': 'post',
                                'text': post_text,
                                'scraped_at': datetime.utcnow().isoformat()
                            })
                    
                    else:  # It's likely a comment
                        comment_elem = content_elem.find('div', class_='usertext-body')
                        if comment_elem:
                            comment_text = comment_elem.get_text(strip=True)
                            if comment_text and len(comment_text) > 10:
                                comments_data.append({
                                    'type': 'comment',
                                    'text': comment_text,
                                    'scraped_at': datetime.utcnow().isoformat()
                                })
                
                except Exception as e:
                    logger.warning(f"Error extracting content element: {str(e)}")
                    continue
            
            return profile_data, posts_data, comments_data
            
        except Exception as e:
            logger.warning(f"Error extracting old Reddit data: {str(e)}")
            return {'username': username, 'karma': 0}, [], []
    
    def _extract_reddit_data(self, soup, username):
        """Extract profile data from new Reddit (limited due to React/JS loading)"""
        try:
            # New Reddit loads content dynamically with JavaScript
            # Very limited scraping capability
            profile_data = {'username': username, 'karma': 0}
            posts_data = []
            comments_data = []
            
            # Try to find any text content
            text_elements = soup.find_all('p')
            content_count = 0
            
            for elem in text_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 20 and content_count < 10:  # Get some content
                    posts_data.append({
                        'type': 'content',
                        'text': text,
                        'scraped_at': datetime.utcnow().isoformat()
                    })
                    content_count += 1
            
            return profile_data, posts_data, comments_data
            
        except Exception as e:
            logger.warning(f"Error extracting Reddit data: {str(e)}")
            return {'username': username, 'karma': 0}, [], []
    
    def get_user_content_text(self, reddit_username, limit=20):
        """Get text content from recent posts and comments for AI analysis"""
        try:
            username = reddit_username.lstrip('u/')
            if username.startswith('/'):
                username = username[1:]
            
            # Try old Reddit first for better access
            url = f"https://old.reddit.com/user/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                _, posts_data, comments_data = self._extract_old_reddit_data(soup, username)
                
                all_content = posts_data + comments_data
                return [item['text'] for item in all_content[:limit]]
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting Reddit content text: {str(e)}")
            return []
