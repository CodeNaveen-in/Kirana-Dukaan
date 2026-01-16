from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from models import db, User, Category, Product, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

# Create a Blueprint object
main = Blueprint('main', __name__)

# BASIC ROUTES
@main.route('/')
def index():
    # 1. Check if user is logged in
    if 'user_id' in session:
        # 2. Fetch the actual user object from the DB using the session ID
        user = User.query.get(session['user_id'])
        
        # 3. If they are an admin, send them to the admin dashboard
        if user and user.is_admin:
            return redirect(url_for('main.admin'))
        
        # 4. Otherwise, show them the standard homepage
        return render_template("index.html", name=user.name)

    # 5. If not logged in at all, send to login
    flash('Please log in to access the store.', 'warning')
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    return render_template("homepage.html")

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/login', methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.passhash, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('main.login'))
    
    # Meant to create an user session and store it, you can store anything we are storing user id 
    session['user_id'] = user.id 
    flash('You have successfully logged in!', 'success')
    if user.is_admin:
        return redirect(url_for('main.admin'))
    return redirect(url_for('main.index'))

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/register', methods=["POST"])
def register_post():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if (not username or not email or not password or not confirm_password):
        flash('Please fill in the important fields', 'danger')
        return redirect(url_for('main.register'))
    
    if (password != confirm_password):
        flash('Passwords do not match', 'danger')
        return redirect(url_for('main.register'))
    
    user = User.query.filter_by(username=username).first()

    if user:
        flash('Username already exists', 'warning')
        return redirect(url_for('main.register'))
    
    passhash = generate_password_hash(password)
    new_user = User(username=username, passhash=passhash, name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful. Please log in.', 'success')
    return redirect(url_for('main.login'))


# Change your other @app.route to @main.route...

# IMPORTANT FUNCTIONS
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/profile')
@auth_required
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@main.route("/profile", methods=["POST"])
@auth_required
def profile_edit():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')

    if not username or not cpassword or not password:
        flash('Please fill out all the required fields', 'danger')
        return redirect(url_for('main.profile'))
    
    user = User.query.get(session['user_id'])
    if not check_password_hash(user.passhash, cpassword):
        flash('Incorrect password', 'danger')
        return redirect(url_for('main.profile'))
    
    if username != user.username:
        new_username = User.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists', 'warning')
            return redirect(url_for('main.profile'))
    
    new_password_hash = generate_password_hash(password)
    user.username = username
    user.passhash = new_password_hash
    user.name = name
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('main.profile'))

@main.route("/logout")
@auth_required
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

# ADMIN PAGES
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('main.login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/admin')
@admin_required
def admin():
    users = User.query.limit(5).all()
    products = Product.query.limit(5).all()
    categories = Category.query.limit(5).all()
    transactions = Transaction.query.order_by(Transaction.datetime.desc()).limit(5).all()
    return render_template('admin.html', users=users, products=products, categories=categories, transactions=transactions)

# Category Management Routes

@main.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.query.all()
    return render_template('category/admin_categories.html', categories=categories)

@main.route('/admin/categories/add', methods=['GET', 'POST'])
@admin_required
def admin_add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Category name is required.', 'danger')
            return redirect(url_for('main.admin_add_category'))
        
        # Check if category already exists
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash('Category already exists.', 'warning')
            return redirect(url_for('main.admin_add_category'))
        
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('main.admin_categories'))
    
    return render_template('category/admin_add_category.html')

@main.route('/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Category name is required.', 'danger')
            return redirect(url_for('main.admin_edit_category', category_id=category_id))
        
        # Check if another category with this name exists
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category and existing_category.id != category_id:
            flash('Category name already exists.', 'warning')
            return redirect(url_for('main.admin_edit_category', category_id=category_id))
        
        category.name = name
        db.session.commit()
        flash('Category updated successfully.', 'success')
        return redirect(url_for('main.admin_categories'))
    
    return render_template('category/admin_edit_category.html', category=category)

@main.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    # Check if category has products
    if category.products:
        flash('Cannot delete category with existing products.', 'danger')
        return redirect(url_for('main.admin_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'success')
    return redirect(url_for('main.admin_categories'))

# Product Management Routes

@main.route('/admin/products')
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('product/admin_products.html', products=products)

@main.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        quantity = request.form.get('quantity')
        man_date = request.form.get('man_date')

        if not all([name, price, description, category_id, quantity, man_date]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.admin_add_product'))
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash('Invalid price or quantity.', 'danger')
            return redirect(url_for('main.admin_add_product'))
        
        category = Category.query.get(category_id)
        if not category:
            flash('Invalid category.', 'danger')
            return redirect(url_for('main.admin_add_product'))
        
        try:
            man_date_obj = datetime.strptime(man_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid manufacturing date.', 'danger')
            return redirect(url_for('main.admin_add_product'))
        
        new_product = Product(
            name=name,
            price=price,
            description=description,
            category_id=category_id,
            quantity=quantity,
            man_date=man_date_obj
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('main.admin_products'))
    
    categories = Category.query.all()
    return render_template('product/admin_add_product.html', categories=categories)

@main.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        quantity = request.form.get('quantity')
        man_date = request.form.get('man_date')

        if not all([name, price, description, category_id, quantity, man_date]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.admin_edit_product', product_id=product_id))
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash('Invalid price or quantity.', 'danger')
            return redirect(url_for('main.admin_edit_product', product_id=product_id))
        
        category = Category.query.get(category_id)
        if not category:
            flash('Invalid category.', 'danger')
            return redirect(url_for('main.admin_edit_product', product_id=product_id))
        
        from datetime import datetime
        try:
            man_date_obj = datetime.strptime(man_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid manufacturing date.', 'danger')
            return redirect(url_for('main.admin_edit_product', product_id=product_id))
        
        product.name = name
        product.price = price
        product.description = description
        product.category_id = category_id
        product.quantity = quantity
        product.man_date = man_date_obj
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('main.admin_products'))
    
    categories = Category.query.all()
    return render_template('product/admin_edit_product.html', product=product, categories=categories)

@main.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product is in cart or has orders
    if product.cart_items or product.orders:
        flash('Cannot delete product that is in carts or has been ordered.', 'danger')
        return redirect(url_for('main.admin_products'))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('main.admin_products'))

# User Management Routes

@main.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('user/admin_users.html', users=users)

@main.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('main.admin_users'))
    
    # Check if user has transactions
    if user.transactions:
        flash('Cannot delete user with transaction history.', 'danger')
        return redirect(url_for('main.admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('main.admin_users'))