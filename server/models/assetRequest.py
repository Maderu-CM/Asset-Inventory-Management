from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AssetRequest(db.Model):
    __tablename__ = 'asset_requests'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)  # Add the asset_name field
    request_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)  # 'low', 'medium', 'high'
    status = db.Column(db.String(20), nullable=False)  # 'pending', 'approved', 'rejected'

    comments = db.relationship('RequestComment', backref='request', lazy=True)
