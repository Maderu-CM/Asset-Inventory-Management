from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, asset, assetAllocation, assetRequest, user, assetCategory
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.dbconfig import db
from models.dbconfig import CloudinaryConfig, SQLAlchemyConfig
from models.user import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
import jwt
import traceback

    # Helper function to get the current user ID
def get_current_user_id():
    return get_jwt_identity()

    from flask_jwt_extended import jwt_required, get_jwt_identity

    # ...

    # Route to add a new asset (for Admin and Procurement Manager)
    @app.route('/assets', methods=['POST'])
    @jwt_required
    def add_asset():
        current_user_id = get_jwt_identity()
    # Check the user's role to ensure they are Admin or Procurement Manager
    user = user.query.get(current_user_id)
    if user.role not in ('Admin', 'Procurement Manager'):
        return jsonify(message='Unauthorized: Only Admin and Procurement Manager can add assets'), 403
    # Implement logic to add a new asset
    asset_data = request.get_json()
    name = asset_data.get('name')
    description = asset_data.get('description')
    category_name = asset_data.get('category_name') # Use category_name instead of category_id
    image_url = asset_data.get('image_url')
    status = asset_data.get('status')
    if not name or not category_name:
        return jsonify(message='Asset name and category name are required'), 400
    # Check if the category exists
    category = assetCategory.query.filter_by(name=category_name).first()
    if not category:
        return jsonify(message='Category not found'), 404

    # Create and add the asset
    asset = asset(name=name, description=description, category=category, image_url=image_url, status=status)
    db.session.add(asset)
    db.session.commit()
    return jsonify(message='Asset added successfully'), 201

    # Route to update asset information (for Admin and Procurement Manager)
    @app.route('/assets/<int:asset_id>', methods=['PUT'])
    @jwt_required
    def update_asset(asset_id):
        current_user_id = get_jwt_identity()

    # Check the user's role to ensure they are Admin or Procurement Manager
    user = user.query.get(current_user_id)
    if user.role not in ('Admin', 'Procurement Manager'):
        return jsonify(message='Unauthorized: Only Admin and Procurement Manager can update assets'), 403

    asset = asset.query.get(asset_id)
    if not asset:
        return jsonify(message='Asset not found'), 404

    asset_data = request.get_json()
    asset.name = asset_data.get('name', asset.name)
    asset.description = asset_data.get('description', asset.description)
    category_name = asset_data.get('category_name')
    if category_name:
        category = assetCategory.query.filter_by(name=category_name).first()
    if not category:
        return jsonify(message='Category not found'), 404
    asset.category = category
    asset.image_url = asset_data.get('image_url', asset.image_url)
    asset.status = asset_data.get('status', asset.status)

    db.session.commit()
    return jsonify(message='Asset updated successfully')

    @app.route('/assets/<int:asset_id>', methods=['DELETE'])
    @jwt_required
    def remove_asset(asset_id):
        current_user_id = get_jwt_identity()

    # Check the user's role to ensure they are Admin or Procurement Manager
    user = user.query.get(current_user_id)
    if user.role not in ('Admin', 'Procurement Manager'):
        return jsonify(message='Unauthorized: Only Admin and Procurement Manager can remove assets'), 403

    asset = asset.query.get(asset_id)
    if not asset:
        return jsonify(message='Asset not found'), 404

    db.session.delete(asset)
    db.session.commit()
    return jsonify(message='Asset removed successfully')

    # Route to allocate an asset to an employee (for Managers)

    @app.route('/allocation', methods=['POST'])
    @jwt_required
    def allocate_asset():
        current_user_id = get_jwt_identity()

    # Check the user's role to ensure they are Admin or Procurement Manager
    user = user.query.get(current_user_id)
    if user.role not in ('Admin', 'Procurement Manager'):
        return jsonify(message='Unauthorized: Only Admin and Procurement Manager can allocate assets'), 403

    allocation_data = request.get_json()
    username = allocation_data.get('username')
    asset_name = allocation_data.get('asset_name')
    allocation_date = allocation_data.get('allocation_date')
    return_date = allocation_data.get('return_date')

    if not username or not asset_name or not allocation_date:
        return jsonify(message='Username, asset name, and allocation date are required'), 400

    # Ensure that both the user and asset exist
    user = user.query.filter_by(username=username).first()
    asset = asset.query.filter_by(name=asset_name).first()

    if not user:
        return jsonify(message='User not found'), 404

    if not asset:
        return jsonify(message='Asset not found'), 404

    allocation = assetAllocation(
    username=username,
    asset_name=asset_name,
    allocation_date=allocation_date,
    return_date=return_date
    )

    db.session.add(allocation)
    db.session.commit()

    return jsonify(message='Asset allocated successfully'), 201

    # Route to submit a request for a new asset or repair (for Users)
    @app.route('/requests', methods=['POST'])
    @jwt_required
    def create_asset_request():
        current_user_id = get_jwt_identity()

    # Implement logic to submit a request for a new asset or repair
    request_data = request.get_json()
    username = user.query.get(current_user_id).username
    asset_name = db.Column(db.String(100), nullable=False)
    request_date = request_data.get('request_date')
    reason = request_data.get('reason')
    quantity = request_data.get('quantity')
    urgency = request_data.get('urgency')
    status = 'pending' # Set the default status to 'pending'

    if not request_date or not reason or not quantity or not urgency:
        return jsonify(message='Request date, reason, quantity, and urgency are required'), 400

    asset_request = assetRequest(
    username=username,
    sset_name= asset_name,
    request_date=request_date,
    reason=reason,
    quantity=quantity,
    urgency=urgency,
    status=status
    )

    db.session.add(asset_request)
    db.session.commit()

    return jsonify(message='Request submitted successfully'), 201

    # Route to review and approve a request (for Procurement Manager)
    @app.route('/requests/<int:request_id>/review', methods=['PUT'])
    @jwt_required
    def review_asset_request(request_id):
    # Get the asset request by ID
     asset_request = assetRequest.query.get(request_id)

    if not asset_request:
        return jsonify(message='Request not found'), 404

    # Check if the user has the Procurement Manager role
    current_user = get_current_user()

    if not current_user or current_user.role != 'Procurement Manager':
        return jsonify(message='Unauthorized: Only Procurement Manager can review and approve requests'), 403

    # Update the request status to "approved"
    asset_request.status = 'approved'
    db.session.commit()

    return jsonify(message='Request reviewed and approved')

    def get_current_user():
    # Implement your logic to get the current user
        current_user = None

    if 'user' in get_jwt_identity():
        user_id = get_jwt_identity()['user_id']
    # Query your user model by user_id to get the user object
    current_user = user.query.get(user_id)

    return current_user 

    # Route to retrieve all pending requests with their urgency (for Procurement Manager)
    @app.route('/requests/pending', methods=['GET'])
    @jwt_required
    def get_pending_requests():
    # Query the database to get pending requests
        pending_requests = assetRequest.query.filter_by(status='pending').all()

    # Create a list to store the details of pending requests
    pending_requests_details = []

    # Iterate through the pending requests and extract their details
    for request in pending_requests:
        request_details = {
    'id': request.id,
    'username': request.username,
    'asset_name': request.asset_name,
    'request_date': request.request_date.strftime('%Y-%m-%d %H:%M:%S'),
    'reason': request.reason,
    'quantity': request.quantity,
    'urgency': request.urgency,
    'status': request.status,
    'comments': [comment.text for comment in request.comments]
    }
    pending_requests_details.append(request_details)

    return jsonify(pending_requests=pending_requests_details)

    # Route to retrieve all completed requests (for Managers)
    @app.route('/requests/completed', methods=['GET'])
    @jwt_required
    def get_completed_requests():
    # Query the database to get completed requests
        completed_requests = assetRequest.query.filter_by(status='completed').all()

    # Create a list to store the details of completed requests
    completed_requests_details = []

    # Iterate through the completed requests and extract their details
    for request in completed_requests:
        request_details = {
    'id': request.id,
    'username': request.username,
    'asset_name': request.asset_name,
    'request_date': request.request_date.strftime('%Y-%m-%d %H:%M:%S'),
    'reason': request.reason,
    'quantity': request.quantity,
    'urgency': request.urgency,
    'status': request.status,
    'comments': [comment.text for comment in request.comments]
    }
    completed_requests_details.append(request_details)

    return jsonify(completed_requests=completed_requests_details)

    # Route to retrieve user-specific request history (for Users)
    @app.route('/requests/user', methods=['GET'])
    @jwt_required
    def get_user_request_history():
    # Get the user's ID based on your application's authentication mechanism
        current_user_id = get_current_user_id()

    # Query the database to get the user's request history
    user_requests = assetRequest.query.filter_by(username=current_user_id).all()

    # Create a list to store the details of the user's request history
    user_requests_details = []

    # Iterate through the user's requests and extract their details
    for request in user_requests:
        request_details = {
    'id': request.id,
    'asset_name': request.asset_name,
    'request_date': request.request_date.strftime('%Y-%m-%d %H:%M:%S'),
    'reason': request.reason,
    'quantity': request.quantity,
    'urgency': request.urgency,
    'status': request.status,
    'comments': [comment.text for comment in request.comments]
    }
    user_requests_details.append(request_details)

    return jsonify(user_request_history=user_requests_details)

    # Route to retrieve all active requests for the current user (for Users)
    @app.route('/profile/active-requests', methods=['GET'])
    @jwt_required
    def get_user_active_requests():
    # Get the user's ID based on your application's authentication mechanism
        current_user_id = get_current_user_id()

    # Query the database to get the user's active requests (status="pending")
    active_requests = assetRequest.query.filter_by(username=current_user_id, status='pending').all()

    # Create a list to store the details of the user's active requests
    active_requests_details = []

    # Iterate through the user's active requests and extract their details
    for request in active_requests:
        request_details = {
    'id': request.id,
    'asset_name': request.asset_name,
    'request_date': request.request_date.strftime('%Y-%m-%d %H:%M:%S'),
    'reason': request.reason,
    'quantity': request.quantity,
    'urgency': request.urgency,
    'status': request.status,
    'comments': [comment.text for comment in request.comments]
    }
    active_requests_details.append(request_details)

    return jsonify(user_active_requests=active_requests_details)

