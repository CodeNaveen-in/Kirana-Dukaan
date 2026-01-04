from flask import Flask, render_template
from app import app

@app.route('/')
def index():
    return render_template("index.html", name="Naveen")

@app.route('/home')
def home():
    return render_template("homepage.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/past-order')
def past():
    return render_template("past-order.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/admin-home")
def admin_home():
    return render_template("admin-home.html")

@app.route("/admin-productpage")
def admin_productpage():
    return render_template("admin-productpage.html")

@app.route("/admin-userspage")
def admin_userspage():
    return render_template("admin-userpage.html")