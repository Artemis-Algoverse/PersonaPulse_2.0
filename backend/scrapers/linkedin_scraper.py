import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from models import db, UserProfile, ScrapingLog
import logging

logger = logging.getLogger(__name__)

class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        # Set user agent to appear as a regular browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_profile(self, linkedin_profile_url, unique_persona_pulse_id):
        """Scrape LinkedIn profile data (public data only)"""
        try:
            # Clean URL if needed
            if not linkedin_profile_url.startswith('http'):
                if linkedin_profile_url.startswith('linkedin.com'):
                    linkedin_profile_url = 'https://' + linkedin_profile_url
                elif not linkedin_profile_url.startswith('/'):
                    linkedin_profile_url = 'https://linkedin.com/in/' + linkedin_profile_url
                else:
                    linkedin_profile_url = 'https://linkedin.com' + linkedin_profile_url
            
            # Make request to public profile
            response = self.session.get(linkedin_profile_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic public information
            about_section = ""
            connections = 0
            headline = ""
            
            try:
                # Try to extract headline
                headline_element = soup.find('h2', class_='text-heading-xlarge')
                if headline_element:
                    headline = headline_element.get_text(strip=True)
            except Exception as e:
                logger.warning(f"Could not extract headline: {str(e)}")
            
            try:
                # Try to extract about section (this is very limited without login)
                # LinkedIn heavily restricts public access to detailed profile information
                about_elements = soup.find_all('section', class_='summary')
                if about_elements:
                    about_section = about_elements[0].get_text(strip=True)
            except Exception as e:
                logger.warning(f"Could not extract about section: {str(e)}")
            
            # Note: LinkedIn severely limits public data access
            # Most profile information requires authentication
            
            # Update database with limited available data
            user_profile = UserProfile.query.filter_by(unique_persona_pulse_id=unique_persona_pulse_id).first()
            if user_profile:
                user_profile.linkedin_id = linkedin_profile_url
                user_profile.linkedin_about = about_section or headline or linkedin_profile_url  # Always store something
                user_profile.linkedin_connections = connections
                user_profile.last_updated = datetime.utcnow()
                db.session.commit()
                log = ScrapingLog(
                    unique_persona_pulse_id=unique_persona_pulse_id,
                    platform='linkedin',
                    status='success' if (about_section or headline) else 'partial',
                    items_scraped=1 if (about_section or headline) else 0,
                    error_message='Limited public data available without authentication'
                )
                db.session.add(log)
                db.session.commit()
                
                logger.info(f"Successfully scraped LinkedIn profile (limited data): {linkedin_profile_url}")
                return True
                
        except Exception as e:
            logger.error(f"Error scraping LinkedIn profile {linkedin_profile_url}: {str(e)}")
            
            # Log error
            log = ScrapingLog(
                unique_persona_pulse_id=unique_persona_pulse_id,
                platform='linkedin',
                status='failed',
                error_message=str(e),
                items_scraped=0
            )
            db.session.add(log)
            db.session.commit()
            
            return False
    
    def get_profile_about_text(self, linkedin_profile_url):
        """Get about section text for AI analysis (limited public data)"""
        try:
            response = self.session.get(linkedin_profile_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract any available text content
            text_elements = soup.find_all(['h1', 'h2', 'h3', 'p'])
            combined_text = ' '.join([elem.get_text(strip=True) for elem in text_elements])
            
            return combined_text[:500]  # Limit text length
            
        except Exception as e:
            logger.error(f"Error getting LinkedIn about text: {str(e)}")
            return ""
    
    def close(self):
        """Close the session"""
        self.session.close()
