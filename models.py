from flask_sqlalchemy import SQLAlchemy

# Initialize the extension without the app
db = SQLAlchemy() 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

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
    # category = db.relationship('Category', backref=db.backref('products', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    man_date = db.Column(db.Date, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

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