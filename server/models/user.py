from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  

    asset_requests = db.relationship('AssetRequest', backref='requester', lazy=True)
    asset_allocations = db.relationship('AssetAllocation', backref='user', lazy=True)

    def __init__(self, username, email, password, role):
            self.username = username
            self.email = email
            self.password = password
            self.role = role