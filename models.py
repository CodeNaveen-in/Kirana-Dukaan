from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Initialize the extension without the app
db = SQLAlchemy() 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    # 1. ADMIN CHECK: A helper property to easily check roles in routes
    @property
    def is_administrator(self):
        return self.is_admin

    # 2. ADMIN CREATION: Encapsulated logic to seed the admin
    @staticmethod
    def ensure_admin_exists():
        # Check if any user with is_admin=True already exists
        admin = User.query.filter_by(is_admin=True).first()
        
        if not admin:
            print("No admin found. Creating default admin account...")
            default_admin = User(
                username="admin",
                passhash=generate_password_hash("admin123"), # Hardcoded password
                name="System Administrator",
                email="admin@kirana.com",
                is_admin=True
            )
            db.session.add(default_admin)
            db.session.commit()
            print("Admin created successfully.")
        else:
            print(f"Admin already exists: {admin.username}")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category relationship is defined via backref in Category model
    quantity = db.Column(db.Integer, nullable=False)
    man_date = db.Column(db.Date, nullable=False)
    cart_items = db.relationship('Cart', backref='product', lazy=True)
    orders = db.relationship('Order', backref='product', lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='cart_items', lazy=True)
    # product relationship is already defined in Product model with backref='product'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    orders = db.relationship('Order', backref='transaction', lazy=True, cascade='all, delete-orphan')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)