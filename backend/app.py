import sqlite3
import json
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

    @app.route('/api/users/dynamic_profile', methods=['POST'])
    def dynamic_profile():
        try:
            data = request.get_json()
            # Accept social profile info (usernames/urls)
            social_media_ids = {
                'instagram': data.get('instagram'),
                'twitter': data.get('twitter'),
                'linkedin': data.get('linkedin'),
                'reddit': data.get('reddit'),
                'social_trait': data.get('social_trait')
            }
            # Create user, scrape, and analyze in one step
            result = persona_service.process_new_user(social_media_ids)
            if not result:
                return jsonify({'error': 'Failed to process user'}), 500
            return jsonify({'message': 'User profile created and analyzed', 'data': result}), 201
        except Exception as e:
            logger.error(f"Error in dynamic_profile: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/users/<unique_id>/keywords', methods=['GET'])
    def get_user_keywords(unique_id):
        try:
            # Fetch personality data from personapulse.db
            from models import PersonalityData
            personality_data = PersonalityData.query.filter_by(unique_persona_pulse_id=unique_id).first()
            if not personality_data:
                return jsonify({'error': 'No personality data found'}), 404
            # Extract keywords from list_of_interest_keywords
            keywords_list = []
            try:
                keywords_list = json.loads(personality_data.list_of_interest_keywords)
            except Exception:
                keywords_list = []
            keywords = ', '.join(keywords_list)
            return jsonify({'keywords': keywords})
        except Exception as e:
            logger.error(f"Error in get_user_keywords: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/events/debug', methods=['GET'])
    def debug_events():
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(events)")
        columns = [row[1] for row in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM events")
        count = cur.fetchone()[0]
        conn.close()
        return jsonify({
            'columns': columns,
            'event_count': count
        })

    # Create instance directory
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # Configure database
    database_path = os.path.join(instance_path, 'personapulse.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS for frontend integration (allow all for dev)
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Initialize services
    persona_service = PersonaPulseService()

    # Initialize scheduler
    scheduler = DataScheduler(app)

    # Event endpoints
    @app.route('/api/events', methods=['POST'])
    def create_event():
        try:
            data = request.get_json()
            title = data.get('title')
            description = data.get('description')
            keywords = data.get('keywords')
            if not title or not description or not keywords:
                return jsonify({'error': 'Missing fields'}), 400
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute('INSERT INTO events (title, description, keywords) VALUES (?, ?, ?)', (title, description, keywords))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Event created successfully'}), 201
        except Exception as e:
            logger.error(f"Error in create_event: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/events', methods=['GET'])
    def get_events():
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute('SELECT id, title, description, keywords FROM events')
            events = cur.fetchall()
            conn.close()
            result = [
                {
                    'id': eid,
                    'title': title,
                    'description': desc,
                    'keywords': kw
                } for eid, title, desc, kw in events
            ]
            return jsonify({'message': 'Events fetched', 'data': result})
        except Exception as e:
            logger.error(f"Error in get_events: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/events/<int:event_id>', methods=['PUT'])
    def update_event(event_id):
        try:
            data = request.get_json()
            title = data.get('title')
            description = data.get('description')
            keywords = data.get('keywords')
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute('UPDATE events SET title=?, description=?, keywords=? WHERE id=?', (title, description, keywords, event_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Event updated successfully'})
        except Exception as e:
            logger.error(f"Error in update_event: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/events/<int:event_id>', methods=['DELETE'])
    def delete_event(event_id):
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute('DELETE FROM events WHERE id=?', (event_id,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Event deleted successfully'})
        except Exception as e:
            logger.error(f"Error in delete_event: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/events/match', methods=['POST'])
    def match_events():
        """Match events based on keywords provided by the frontend"""
        try:
            from event_matching import extract_event_keywords
            data = request.get_json()
            keywords = data.get('keywords', '')
            if not keywords:
                return jsonify({'error': 'No keywords provided'}), 400
            # Support comma-separated or list input
            if isinstance(keywords, str):
                keywords_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
            elif isinstance(keywords, list):
                keywords_list = keywords
            else:
                keywords_list = []
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.db')
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(events)")
            columns = [row[1] for row in cur.fetchall()]
            logger.info(f"Events table columns: {columns}")
            select_cols = [col for col in ['id', 'title', 'description', 'keywords'] if col in columns]
            if not select_cols:
                conn.close()
                return jsonify({'error': 'No valid columns in events table'}), 500
            # Build OR query for all keywords
            where_clauses = []
            params = []
            for kw in keywords_list:
                where_clauses.append("keywords LIKE ?")
                params.append(f'%{kw}%')
            where_sql = ' OR '.join(where_clauses) if where_clauses else '1=0'
            query = f"SELECT {', '.join(select_cols)} FROM events WHERE {where_sql}"
            cur.execute(query, params)
            events = cur.fetchall()
            conn.close()
            result = [dict(zip(select_cols, row)) for row in events]
            return jsonify({'message': 'Events matched', 'data': result})
        except Exception as e:
            logger.error(f"Error in match_events: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    # ...existing user, scheduler, and error handler routes...
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
                'POST /api/scheduler/start': 'Start scheduled updates',
                'GET /api/events': 'Get all events',
                'POST /api/events': 'Create event',
                'PUT /api/events/<id>': 'Update event',
                'DELETE /api/events/<id>': 'Delete event',
                'POST /api/events/match': 'Match events by keywords'
            }
        })

    # ...existing health, user, scheduler, log, and error handler routes...
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
