from . import db, login_manager
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# defent class user
class User(db.Model, UserMixin):
    __tablename__ = "users"
    # users label
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), index=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    confirmed = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    home = db.Column(db.String(128))
    photo_url = db.Column(db.String(128))
    comment = db.relationship("Comment", backref="user", lazy="dynamic")
    msg = db.relationship("Message", backref='user', lazy="dynamic")
    
    # for show User
    def __repr__(self):
        return "<User %s>" % self.username

    # add user's role
    def __init__(self, **kw):
        super(User, self).__init__(**kw)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(is_admin=True).first()
            if self.role is None:
                self.role = Role.query.filter_by(is_admin=False).first()

    # passowrd
    @property
    def password(self):
        return
    # write password
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # confirm password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # email confirm token
    def generate_confirmation_token(self, expiration=600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id})

    # email confirmation
    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            print(1)
            return False
        if data.get("confirm") != self.id:
            print(2)
            return False
        self.confirmed = True
        db.session.add(self)
        return True

# role tabel
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    user = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %s>" % self.name



# comment table
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)
    def __repr__(self):
        return "<Comment>"

# article table
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    title = db.Column(db.String(128), unique=True)
    comment = db.relationship("Comment", backref="article", lazy="dynamic")

    def __repr__(self):
        return "<Article %s>" % self.title

 
# msg table
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), default='Anonymous')
    time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return "<Message %s>" % self.message
