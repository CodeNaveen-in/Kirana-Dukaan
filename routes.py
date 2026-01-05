from flask import Blueprint, render_template, url_for

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

# Change your other @app.route to @main.route...