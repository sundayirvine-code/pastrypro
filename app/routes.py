# routes.py

from flask import Blueprint, render_template, redirect, url_for
from .forms import RegistrationForm, LoginForm

# Create a blueprint for the routes
bp = Blueprint('routes', __name__)

# Define your routes
@bp.route('/')
def home():
    return render_template('index.html')

# Define routes for signup and login
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data (e.g., create a new user)
        # Redirect to a success page or login page
        return redirect(url_for('routes.login'))
    return render_template('signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process the form data (e.g., authenticate user)
        # Redirect to a logged-in page or dashboard
        return redirect(url_for('routes.home'))
    return render_template('login.html', form=form)

@bp.route('/inventory')
def products():
    # Logic to fetch and display products
    return render_template('inventory.html')

# Add more routes as needed
