from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RequestComment(db.Model):
    __tablename__ = 'request_comments'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('asset_requests.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)