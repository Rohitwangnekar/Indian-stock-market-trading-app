import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """All the configurations required to run the web application"""

    # Set SECRET_KEY to sign cookies and for other security related tools
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default_secret_key"

    # Turn on Jinja template reloading
    TEMPLATES_AUTO_RELOAD = True

    # Configure session to use filesystem (instead of signed cookies)
    # SESSION_FILE_DIR = tempfile.mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or ("sqlite:///" + os.path.join(basedir, "finance.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Razorpay configuration
    RAZORPAY_KEY_ID = 'rzp_test_A64tNiZma0xQmT'
    RAZORPAY_KEY_SECRET = 'VlB4mVOMILl3sGxgiFrOhsQ6'
