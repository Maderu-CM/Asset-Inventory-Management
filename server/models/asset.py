from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False)  # 'available', 'in repair', 'allocated'

    category = db.relationship('AssetCategory', foreign_keys=[category_name], lazy=True)
    allocations = db.relationship('AssetAllocation', backref='asset', lazy=True)
    requests = db.relationship('AssetRequest', backref='asset', lazy=True)
