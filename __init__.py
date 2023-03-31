from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager


from auth import auth
from main import main
from changeprofile import changeprof

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(changeprof)

app.secret_key = 'JS8dk0JH9sk0s021M8dk2jOhujd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evidence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.max_content_length = 1024 * 1024
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    textFor = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return 'Article %r' % self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
