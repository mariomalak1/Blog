from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from appname.conifg import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
by = Bcrypt(app)
login_manger = LoginManager(app)
                          # function name  of routes
login_manger.login_view = 'users.login'

login_manger.login_message_category = 'warning'

mail = Mail(app)

from appname.posts.routes import posts
from appname.users.routes import users
from appname.main.routes import main
from appname.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)


