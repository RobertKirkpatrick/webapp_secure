from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
# inform flask login which view function handles logins, which is the name used in a url_for() call to get the URL.
login.login_view = 'login'
db.init_app(app)
migrate = Migrate(app, db)

from app import routes, models
db.create_all()
db.session.commit()