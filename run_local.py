#!/usr/bin/env python3
"""
🚀 Local Development Runner for Indian Stock Market Trading App

This script runs the app with embedded API keys for local development.
⚠️  WARNING: For local development only - NOT for production!

Usage:
    python3 run_local.py
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import local configuration
from config_local import DevelopmentConfig

def create_app():
    """Create and configure the Flask app for local development"""
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # Import models
    from finance.models import User, Transaction, Contact, Order
    
    # Create a custom finance module context
    import finance
    finance.app = app
    finance.db = db
    
    # Import routes (this will register all routes)
    from finance import routes
    
    return app, db

def main():
    """Main function to run the local development server"""
    print("=" * 60)
    print("🇮🇳 Indian Stock Market Trading App - LOCAL DEVELOPMENT")
    print("=" * 60)
    print("🚨 WARNING: Running with embedded API keys!")
    print("📍 This is for LOCAL DEVELOPMENT ONLY")
    print("🔒 Do NOT use in production or public deployment")
    print("🌐 App will be available at: http://localhost:5000")
    print("=" * 60)
    
    # Create the app
    app, db = create_app()
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return
    
    # Display configuration info
    print("\n📋 Current Configuration:")
    print(f"   • Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    print(f"   • Secret Key: {'Set' if app.config.get('SECRET_KEY') else 'Not set'}")
    print(f"   • Razorpay Key: {'Set' if app.config.get('RAZORPAY_KEY_ID') else 'Not set'}")
    print(f"   • Alpha Vantage Key: {'Set' if app.config.get('ALPHA_VANTAGE_API_KEY') else 'Not set'}")
    print(f"   • News API Key: {'Set' if app.config.get('NEWS_API_KEY') else 'Not set'}")
    print("\n🚀 Starting development server...")
    print("   Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Run the development server
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == '__main__':
    main()