# routes.py

from flask import Blueprint, render_template

# Create a blueprint for the routes
bp = Blueprint('routes', __name__)

# Define your routes
@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/products')
def products():
    # Logic to fetch and display products
    return render_template('products.html')

# Add more routes as needed
