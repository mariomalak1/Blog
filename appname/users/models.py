from appname import db, login_manger, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as seri


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(40), nullable = False, unique=True)
    password = db.Column(db.String(140), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique= True)
    image_file = db.Column(db.String(200), default = "default.jpg", nullable = False)
    posts = db.relationship('Post', backref = "author", lazy = True)
    admin = db.Column(db.BOOLEAN, nullable= True, default= False)

    def get_reset_token(self, expires_sec = 1800):
        s = seri(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")


    @staticmethod
    def verify_reset_token(token):
        s = seri(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            print("hg none")
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"