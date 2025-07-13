import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Local development configuration with API keys included for convenience"""

    # Set SECRET_KEY to sign cookies and for other security related tools
    SECRET_KEY = "dev_secret_key_for_local_testing_only_change_in_production"

    # Turn on Jinja template reloading
    TEMPLATES_AUTO_RELOAD = True

    # Configure session to use filesystem (instead of signed cookies)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or ("sqlite:///" + os.path.join(basedir, "finance.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ⚠️ LOCAL DEVELOPMENT API KEYS - DO NOT USE IN PRODUCTION ⚠️
    # These are test/demo keys for local development only
    
    # Razorpay TEST credentials (for local development only)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_test_A64tNiZma0xQmT'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'VlB4mVOMILl3sGxgiFrOhsQ6'
    
    # Alpha Vantage API Key (Demo key - replace with your own)
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY') or 'E04K4FQGMADSGN2A'
    
    # News API Key (Demo key - replace with your own)
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'your_news_api_key_here'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration - ALWAYS uses environment variables"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Override to FORCE environment variables in production
    SECRET_KEY = os.environ.get("SECRET_KEY")
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}