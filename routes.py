from flask import Blueprint, render_template, url_for, request, redirect, flash
from models import db, User, Category
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint object
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html", name="Naveen")

@main.route('/home')
def home():
    return render_template("homepage.html")

@main.route('/login')
def login():
    return render_template('login.html')

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
        flash('Please fill in the important Fields')
        return redirect(url_for('main.register'))
    
    if (password != confirm_password):
        flash('Passwords do not match')
        return redirect(url_for('main.register'))
    
    user = User.query.filter_by(username=username).first()

    if user:
        flash('Username already exists')
        return redirect(url_for('main.register'))
    
    passhash = generate_password_hash(password)
    new_user = User(username=username, passhash=passhash, name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.login'))


# Change your other @app.route to @main.route...