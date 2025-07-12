import flask
import flask_sqlalchemy
import flask_migrate
from flask_mail import Mail
import config

app = flask.Flask(__name__)
app.config.from_object(config.Config)

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
mail = Mail(app)

from finance import routes
