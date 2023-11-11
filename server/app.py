from flask import Flask, request, jsonify
from cloudinary.uploader import upload
import cloudinary
from flask_migrate import Migrate
from models.dbconfig import db
from models.asset import Asset
from models.assetAllocation import AssetAllocation
from models.assetRequest import AssetRequest
from models.user  import User
from models.PasswordResetToken import PasswordResetToken
from models.assetCategory import AssetCategory
from routes import create_app
from models.dbconfig import CloudinaryConfig, SQLAlchemyConfig

# App initialization
app = create_app()

# Configure Cloudinary
cloudinary.config(
    cloud_name=CloudinaryConfig.CLOUDINARY_CLOUD_NAME,
    api_key=CloudinaryConfig.CLOUDINARY_API_KEY,
    api_secret=CloudinaryConfig.CLOUDINARY_API_SECRET,
)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = SQLAlchemyConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLAlchemyConfig.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the upload route
@app.route("/upload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            return jsonify(upload_result)
