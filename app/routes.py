# routes.py

from flask import Blueprint, render_template

# Create a blueprint for the routes
bp = Blueprint('routes', __name__)

# Define your routes
@bp.route('/')
def home():
    return render_template('index.html')

# Define routes for signup and login
@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/inventory')
def products():
    # Logic to fetch and display products
    return render_template('inventory.html')

# Add more routes as needed
