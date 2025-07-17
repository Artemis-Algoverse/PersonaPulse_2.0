import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, UserProfile, PersonalityData, ScrapingLog
from services import PersonaPulseService
from scheduler import DataScheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Create instance directory
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Configure database
    database_path = os.path.join(instance_path, 'personapulse.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS for frontend integration
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    # Initialize database
    db.init_app(app)
    
    # Initialize services
    persona_service = PersonaPulseService()
    
    # Initialize scheduler
    scheduler = DataScheduler(app)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'PersonaPulse API v1.0',
            'description': 'Social Media Personality Analysis Platform',
            'endpoints': {
                'POST /api/users': 'Create new user profile',
                'GET /api/users': 'Get all users',
                'GET /api/users/<id>': 'Get specific user profile',
                'POST /api/users/<id>/scrape': 'Manually trigger data scraping',
                'POST /api/users/<id>/analyze': 'Manually trigger personality analysis',
                'GET /api/scheduler/status': 'Get scheduler job status',
                'POST /api/scheduler/start': 'Start scheduled updates'
            }
        })
    
    @app.route('/api/users', methods=['POST'])
    def create_user():
        """Create a new user profile and process their data"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Validate required social media IDs
            social_media_ids = {}
            if 'instagram' in data:
                social_media_ids['instagram'] = data['instagram']
            if 'twitter' in data:
                social_media_ids['twitter'] = data['twitter']
            if 'reddit' in data:
                social_media_ids['reddit'] = data['reddit']
            if 'linkedin' in data:
                social_media_ids['linkedin'] = data['linkedin']
            
            if not social_media_ids:
                return jsonify({'error': 'At least one social media ID required'}), 400
            
            # Process user data
            result = persona_service.process_new_user(social_media_ids)
            
            if result:
                return jsonify({
                    'message': 'User created and processed successfully',
                    'data': result
                }), 201
            else:
                return jsonify({'error': 'Failed to process user data'}), 500
                
        except Exception as e:
            logger.error(f"Error in create_user: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/users', methods=['GET'])
    def get_all_users():
        """Get all user profiles"""
        try:
            users = persona_service.get_all_users()
            return jsonify({
                'message': 'Users retrieved successfully',
                'data': users,
                'count': len(users)
            })
            
        except Exception as e:
            logger.error(f"Error in get_all_users: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/users/<unique_id>', methods=['GET'])
    def get_user(unique_id):
        """Get specific user profile"""
        try:
            user = persona_service.get_user_profile(unique_id)
            
            if user:
                return jsonify({
                    'message': 'User retrieved successfully',
                    'data': user
                })
            else:
                return jsonify({'error': 'User not found'}), 404
                
        except Exception as e:
            logger.error(f"Error in get_user: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/users/<unique_id>/scrape', methods=['POST'])
    def manual_scrape(unique_id):
        """Manually trigger data scraping for a user"""
        try:
            result = persona_service.scrape_user_data(unique_id)
            
            if result:
                return jsonify({
                    'message': 'Data scraping completed',
                    'data': result
                })
            else:
                return jsonify({'error': 'Failed to scrape data'}), 500
                
        except Exception as e:
            logger.error(f"Error in manual_scrape: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/users/<unique_id>/analyze', methods=['POST'])
    def manual_analyze(unique_id):
        """Manually trigger personality analysis for a user"""
        try:
            result = persona_service.analyze_user_personality(unique_id)
            
            if result:
                return jsonify({
                    'message': 'Personality analysis completed',
                    'data': result
                })
            else:
                return jsonify({'error': 'Failed to analyze personality'}), 500
                
        except Exception as e:
            logger.error(f"Error in manual_analyze: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/scheduler/status', methods=['GET'])
    def scheduler_status():
        """Get scheduler job status"""
        try:
            status = scheduler.get_job_status()
            return jsonify({
                'message': 'Scheduler status retrieved',
                'data': status
            })
            
        except Exception as e:
            logger.error(f"Error in scheduler_status: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/scheduler/start', methods=['POST'])
    def start_scheduler():
        """Start scheduled daily updates"""
        try:
            scheduler.schedule_daily_update()
            return jsonify({
                'message': 'Scheduled updates started',
                'interval_hours': Config.SCHEDULER_INTERVAL_HOURS
            })
            
        except Exception as e:
            logger.error(f"Error in start_scheduler: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/logs/<unique_id>', methods=['GET'])
    def get_user_logs(unique_id):
        """Get scraping logs for a user"""
        try:
            logs = ScrapingLog.query.filter_by(unique_persona_pulse_id=unique_id).order_by(ScrapingLog.timestamp.desc()).all()
            logs_data = [log.to_dict() for log in logs]
            
            return jsonify({
                'message': 'Logs retrieved successfully',
                'data': logs_data
            })
            
        except Exception as e:
            logger.error(f"Error in get_user_logs: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
