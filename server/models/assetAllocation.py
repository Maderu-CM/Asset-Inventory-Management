from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AssetAllocation(db.Model):
    __tablename__ = 'asset_allocations'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    allocation_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', foreign_keys=[username], backref='asset_allocations')
