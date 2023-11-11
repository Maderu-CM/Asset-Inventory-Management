from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AssetCategory(db.Model):
    __tablename__ = 'asset_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    assets = db.relationship('Asset', backref='category', lazy=True)