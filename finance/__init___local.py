import flask
import flask_sqlalchemy
import flask_migrate
from flask_mail import Mail
import config_local

app = flask.Flask(__name__)

# Use local development configuration
app.config.from_object(config_local.DevelopmentConfig)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
mail = Mail(app)

from finance import routes