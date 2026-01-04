from flask import Blueprint, render_template

# Create a Blueprint object
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html", name="Naveen")

@main.route('/home')
def home():
    return render_template("homepage.html")

# Change your other @app.route to @main.route...