"""
Local Development Version of the Indian Stock Market Trading App
This version includes API keys for local development convenience.

⚠️ WARNING: This is for LOCAL DEVELOPMENT ONLY
Do NOT deploy this to production or push to public repositories!
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config_local import config

# Create Flask app
app = Flask(__name__)

# Load configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to ensure they are known to Flask-Migrate
from finance.models import User, Transaction, Contact, Order

# Import routes
from finance import routes

if __name__ == '__main__':
    print("🚨 WARNING: Running in LOCAL DEVELOPMENT mode with embedded API keys!")
    print("📍 This should ONLY be used for local testing")
    print("🌐 Access the app at: http://localhost:5000")
    print("-" * 60)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )