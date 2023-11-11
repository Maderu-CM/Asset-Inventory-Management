from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models.user import User
from models.asset import Asset, AssetCategory
from models.assetAllocation import AssetAllocation
from models.assetRequest import AssetRequest, RequestComment
from models.PasswordResetToken import PasswordResetToken
from datetime import datetime, timedelta

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'  # Replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create fake users
def create_fake_users(count=10):
    users = []
    for _ in range(count):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            role=fake.random_element(elements=('Admin', 'Procurement Manager', 'User'))
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

# Create fake asset categories
def create_fake_asset_categories(count=5):
    categories = []
    for _ in range(count):
        category = AssetCategory(
            name=fake.unique.first_name()
        )
        categories.append(category)
    db.session.add_all(categories)
    db.session.commit()

# Create fake assets
def create_fake_assets(count=20):
    assets = []
    real_asset_names = ["Laptop", "Desk Chair", "Printer", "Conference Table", "Whiteboard", "Projector", "Office Phone", "Server Rack", "Office Plants", "Filing Cabinet", "Desk", "Monitor", "Air Conditioner", "Refrigerator", "Coffee Machine", "Water Cooler", "Security Camera", "Fire Extinguisher", "First Aid Kit", "Shredder"]

    for _ in range(count):
        asset_name = fake.random_element(elements=real_asset_names)
        description = fake.text(max_nb_chars=250)
        asset = Asset(
            name=asset_name,
            description=description,
            category_name=fake.random_element(AssetCategory.query.all()).name,
            image_url=fake.image_url(),
            status=fake.random_element(elements=('In Use', 'Available', 'Repaired'))
        )
        assets.append(asset)
    db.session.add_all(assets)
    db.session.commit()

# Create fake asset allocations
def create_fake_asset_allocations(count=30):
    allocations = []
    for _ in range(count):
        allocation = AssetAllocation(
            asset_name=fake.random_element(Asset.query.all()).name,
            username=fake.random_element(User.query.all()).username,
            allocation_date=fake.date_time_this_decade(),
            return_date=fake.date_time_this_decade()
        )
        allocations.append(allocation)
    db.session.add_all(allocations)
    db.session.commit()

# Create fake asset requests
def create_fake_asset_requests(count=50):
    requests = []
    for _ in range(count):
        request = AssetRequest(
            username=fake.random_element(User.query.all()).username,
            asset_name=fake.random_element(Asset.query.all()).name,
            request_date=fake.date_time_this_decade(),
            reason=fake.text(max_nb_chars=250),
            quantity=fake.random_int(min=1, max=10),
            urgency=fake.random_element(elements=('High', 'Medium', 'Low')),
            status=fake.random_element(elements=('Pending', 'Approved', 'Rejected')),
            completion_date=fake.date_time_this_decade()
        )
        requests.append(request)
    db.session.add_all(requests)
    db.session.commit()

# Create fake request comments
def create_fake_request_comments(count=20):
    comments = []
    for _ in range(count):
        comment = RequestComment(
            request_id=fake.random_element(AssetRequest.query.all()).id,
            user_id=fake.random_element(User.query.all()).id,
            comment=fake.text(max_nb_chars=250),
            comment_date=fake.date_time_this_decade()
        )
        comments.append(comment)
    db.session.add_all(comments)
    db.session.commit()

# Create fake password reset tokens
def create_fake_password_reset_tokens(count=10):
    tokens = []
    for _ in range(count):
        user = fake.random_element(User.query.all())
        token = PasswordResetToken(
            user_id=user.id,
            token=fake.sha1(),
            expiration=datetime.now() + timedelta(days=fake.random_int(min=1, max=30))
        )
        tokens.append(token)
    db.session.add_all(tokens)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_fake_users()
        create_fake_asset_categories()
        create_fake_assets()
        create_fake_asset_allocations()
        create_fake_asset_requests()
        create_fake_request_comments()
        create_fake_password_reset_tokens()
        print("Database seeded successfully!")
