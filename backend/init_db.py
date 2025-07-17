import os
from flask import Flask
from models import db

# Create instance directory if it doesn't exist
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = Flask(__name__, instance_path=instance_path)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "personapulse.db")}'
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
