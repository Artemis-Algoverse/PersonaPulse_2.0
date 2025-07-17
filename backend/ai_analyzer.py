import google.generativeai as genai
import json
import logging
from datetime import datetime
from models import db, UserProfile, PersonalityData

logger = logging.getLogger(__name__)

class PersonalityAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyze_personality(self, unique_persona_pulse_id):
        """Analyze personality from scraped social media data"""
        try:
            # Get user profile data
            user_profile = UserProfile.query.filter_by(unique_persona_pulse_id=unique_persona_pulse_id).first()
            if not user_profile:
                raise Exception(f"User profile not found for ID: {unique_persona_pulse_id}")
            
            # Prepare data for analysis
            analysis_data = self._prepare_analysis_data(user_profile)
            
            if not analysis_data:
                raise Exception("No social media data available for analysis")
            
            # Create prompt for GenAI
            prompt = self._create_analysis_prompt(analysis_data)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse response
            analysis_result = self._parse_ai_response(response.text)
            
            # Save to database
            self._save_personality_data(unique_persona_pulse_id, analysis_result)
            
            logger.info(f"Successfully analyzed personality for user: {unique_persona_pulse_id}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing personality for {unique_persona_pulse_id}: {str(e)}")
            return None
    
    def _prepare_analysis_data(self, user_profile):
        """Prepare social media data for AI analysis"""
        analysis_data = {
            'instagram': {},
            'twitter': {},
            'linkedin': {},
            'reddit': {}
        }
        
        # Instagram data
        if user_profile.insta_bio:
            analysis_data['instagram']['bio'] = user_profile.insta_bio
        
        if user_profile.insta_posts_hashtags:
            try:
                hashtags = json.loads(user_profile.insta_posts_hashtags)
                analysis_data['instagram']['hashtags'] = hashtags[:20]  # Limit hashtags
            except:
                pass
        
        # Twitter data
        if user_profile.twitter_posts:
            try:
                tweets = json.loads(user_profile.twitter_posts)
                tweet_texts = [tweet['text'] for tweet in tweets[:10]]  # Limit tweets
                analysis_data['twitter']['tweets'] = tweet_texts
            except:
                pass
        
        # LinkedIn data
        if user_profile.linkedin_about:
            analysis_data['linkedin']['about'] = user_profile.linkedin_about
        
        # Reddit data
        if user_profile.reddit_posts:
            try:
                reddit_data = json.loads(user_profile.reddit_posts)
                post_texts = []
                comment_texts = []
                
                # Get post titles and content
                for post in reddit_data.get('posts', [])[:5]:
                    if post.get('title'):
                        post_texts.append(post['title'])
                    if post.get('selftext'):
                        post_texts.append(post['selftext'])
                
                # Get comment texts
                for comment in reddit_data.get('comments', [])[:10]:
                    if comment.get('body'):
                        comment_texts.append(comment['body'])
                
                analysis_data['reddit']['posts'] = post_texts
                analysis_data['reddit']['comments'] = comment_texts
            except:
                pass
        
        return analysis_data
    
    def _create_analysis_prompt(self, analysis_data):
        """Create prompt for GenAI personality analysis"""
        prompt = f"""
You are an expert personality analyst. Analyze the following social media data and provide:

1. A list of interest keywords (10-20 keywords representing the person's interests)
2. OCEAN personality traits scored from 0-100:
   - Openness to Experience (creativity, curiosity, openness to new ideas)
   - Conscientiousness (organization, discipline, responsibility)
   - Extraversion (sociability, assertiveness, energy)
   - Agreeableness (cooperation, trust, empathy)
   - Neuroticism (emotional instability, anxiety, stress)

3. A confidence score (0-100) for your analysis
4. Top 3 dominant personality traits

Social Media Data:
{json.dumps(analysis_data, indent=2)}

Please respond ONLY with a valid JSON object in this exact format:
{{
    "interest_keywords": ["keyword1", "keyword2", ...],
    "ocean_scores": {{
        "openness": 75,
        "conscientiousness": 65,
        "extraversion": 80,
        "agreeableness": 70,
        "neuroticism": 30
    }},
    "confidence_score": 85,
    "dominant_traits": ["trait1", "trait2", "trait3"]
}}

Do not include any other text or explanation outside the JSON object.
"""
        return prompt
    
    def _parse_ai_response(self, response_text):
        """Parse AI response to extract personality data"""
        try:
            # Clean the response text
            response_text = response_text.strip()
            
            # Find JSON content
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise Exception("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['interest_keywords', 'ocean_scores', 'confidence_score', 'dominant_traits']
            for field in required_fields:
                if field not in result:
                    raise Exception(f"Missing required field: {field}")
            
            # Validate OCEAN scores
            ocean_fields = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
            for field in ocean_fields:
                if field not in result['ocean_scores']:
                    raise Exception(f"Missing OCEAN field: {field}")
                
                # Ensure scores are within 0-100 range
                score = result['ocean_scores'][field]
                if not isinstance(score, (int, float)) or score < 0 or score > 100:
                    result['ocean_scores'][field] = max(0, min(100, float(score)))
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            # Return default values if parsing fails
            return {
                "interest_keywords": ["general", "lifestyle"],
                "ocean_scores": {
                    "openness": 50,
                    "conscientiousness": 50,
                    "extraversion": 50,
                    "agreeableness": 50,
                    "neuroticism": 50
                },
                "confidence_score": 20,
                "dominant_traits": ["neutral", "balanced", "moderate"]
            }
    
    def _save_personality_data(self, unique_persona_pulse_id, analysis_result):
        """Save personality analysis results to database"""
        try:
            # Check if personality data already exists
            personality_data = PersonalityData.query.filter_by(
                unique_persona_pulse_id=unique_persona_pulse_id
            ).first()
            
            if personality_data:
                # Update existing record
                personality_data.list_of_interest_keywords = json.dumps(analysis_result['interest_keywords'])
                personality_data.openness = analysis_result['ocean_scores']['openness']
                personality_data.conscientiousness = analysis_result['ocean_scores']['conscientiousness']
                personality_data.extraversion = analysis_result['ocean_scores']['extraversion']
                personality_data.agreeableness = analysis_result['ocean_scores']['agreeableness']
                personality_data.neuroticism = analysis_result['ocean_scores']['neuroticism']
                personality_data.confidence_score = analysis_result['confidence_score']
                personality_data.dominant_traits = ', '.join(analysis_result['dominant_traits'])
                personality_data.last_updated = datetime.utcnow()
            else:
                # Create new record
                personality_data = PersonalityData(
                    unique_persona_pulse_id=unique_persona_pulse_id,
                    list_of_interest_keywords=json.dumps(analysis_result['interest_keywords']),
                    openness=analysis_result['ocean_scores']['openness'],
                    conscientiousness=analysis_result['ocean_scores']['conscientiousness'],
                    extraversion=analysis_result['ocean_scores']['extraversion'],
                    agreeableness=analysis_result['ocean_scores']['agreeableness'],
                    neuroticism=analysis_result['ocean_scores']['neuroticism'],
                    confidence_score=analysis_result['confidence_score'],
                    dominant_traits=', '.join(analysis_result['dominant_traits'])
                )
                db.session.add(personality_data)
            
            db.session.commit()
            logger.info(f"Saved personality data for user: {unique_persona_pulse_id}")
            
        except Exception as e:
            logger.error(f"Error saving personality data: {str(e)}")
            db.session.rollback()
            raise
