from flask import Blueprint, jsonify, request, session
from models import db, User, Product, Category, Transaction
from functools import wraps

api = Blueprint('api', __name__)

def api_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_api_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# User API
@api.route('/users', methods=['GET'])
@admin_api_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'name': u.name,
        'email': u.email,
        'is_admin': u.is_admin
    } for u in users])

@api.route('/users/<int:user_id>', methods=['GET'])
@admin_api_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'is_admin': user.is_admin
    })

# Product API
@api.route('/products', methods=['GET'])
@api_auth_required
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'category_id': p.category_id,
        'category_name': p.category.name if p.category else None,
        'quantity': p.quantity,
        'man_date': p.man_date.isoformat() if p.man_date else None
    } for p in products])

@api.route('/products/<int:product_id>', methods=['GET'])
@api_auth_required
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'category_id': product.category_id,
        'category_name': product.category.name if product.category else None,
        'quantity': product.quantity,
        'man_date': product.man_date.isoformat() if product.man_date else None
    })

# Category API
@api.route('/categories', methods=['GET'])
@api_auth_required
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'product_count': len(c.products)
    } for c in categories])

@api.route('/categories/<int:category_id>', methods=['GET'])
@api_auth_required
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'product_count': len(category.products),
        'products': [{
            'id': p.id,
            'name': p.name,
            'price': p.price
        } for p in category.products]
    })

# Transaction API (Admin only)
@api.route('/transactions', methods=['GET'])
@admin_api_required
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.datetime.desc()).all()
    return jsonify([{
        'id': t.id,
        'user_id': t.user_id,
        'username': t.user.username if t.user else None,
        'datetime': t.datetime.isoformat(),
        'order_count': len(t.orders),
        'total_value': sum(o.price for o in t.orders)
    } for t in transactions])

@api.route('/transactions/<int:transaction_id>', methods=['GET'])
@admin_api_required
def get_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify({
        'id': transaction.id,
        'user_id': transaction.user_id,
        'username': transaction.user.username if transaction.user else None,
        'datetime': transaction.datetime.isoformat(),
        'orders': [{
            'id': o.id,
            'product_id': o.product_id,
            'product_name': o.product.name if o.product else None,
            'quantity': o.quantity,
            'price': o.price
        } for o in transaction.orders]
    })