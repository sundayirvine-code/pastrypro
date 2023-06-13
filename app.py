# app.py file
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, func
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from dotenv import load_dotenv
import pymysql
from forms import RegistrationForm, LoginForm
from decimal import Decimal


# Load environment variables from .env file
load_dotenv()

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '\xce!\x9e\x04\x00\x03\xdf\x88\xf1\x1b@m\xe2\xc6R\xd80\xf6H\x84\xe0e\xc1\x02'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

# Models
class User(UserMixin, db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        is_admin (bool): Indicates whether the user is an admin or not.

    Methods:
        __repr__: Returns a string representation of the User object.
        set_password: Sets the password for the user by generating a hash.
        check_password: Checks if a provided password matches the user's hashed password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    """
    Represents a stock item.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (Decimal): The price of the product.
        quantity (Decimal): The quantity of the product in stock.
        image_id (int): The foreign key to the associated image for the product.
        category_id (int): The foreign key to the associated category for the product.
        user_id (int): The foreign key to the associated user who added the product.
        unit_of_measurement_id (int): The foreign key to the associated unit of measurement for the product.
        unit_of_measurement (UnitOfMeasurement): The relationship to the UnitOfMeasurement object.

    Methods:
        __repr__: Returns a string representation of the Product object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)  
    quantity = db.Column(db.DECIMAL(precision=8, scale=2), default=0.0)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'), nullable=False)
    unit_of_measurement = db.relationship('UnitOfMeasurement')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class Category(db.Model):
    """
    Represents a stock item category.

    Attributes:
        id (int): The unique identifier of the category.
        name (str): The name of the category.
        user_id (int): The foreign key to the associated user who added the category.
        user (User): The relationship to the User object.

    Methods:
        __repr__: Returns a string representation of the Category object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User') 

    def __repr__(self):
        return f"Category('{self.name}')"

class Image(db.Model):
    """
    Represents an image associated with a product.

    Attributes:
        id (int): The unique identifier of the image.
        image_url (str): The URL of the image.

    Methods:
        __repr__: Returns a string representation of the Image object.
    """
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Image('{self.image_url}')"

class UnitOfMeasurement(db.Model):
    """
    Represents a unit of measurement for products.

    Attributes:
        id (int): The unique identifier of the unit of measurement.
        name (str): The name of the unit of measurement.

    Methods:
        None
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

default_units = [
    {'name': 'grams'},
    {'name': 'kilograms'},
    {'name': 'pieces'},
    {'name': 'meters'},
    {'name': 'liters'},
    {'name': 'milliliters'},
    {'name': 'cups'},
    {'name': 'teaspoons'},
    {'name': 'tablespoons'},
    {'name': 'packets'},
    {'name': 'slices'},
    {'name': 'sheets'},
    {'name': 'rolls'},
    {'name': 'bars'},
    {'name': 'cans'},
    {'name': 'bottles'},
    {'name': 'jars'},
    {'name': 'bundles'},
    {'name': 'boxes'},
    # Add more units as needed
]

def seed_unit_of_measurement():
    """
    Seeds the database with default units of measurement.

    This function loads the default units of measurement from the `default_units` list
    and adds them to the database if they don't already exist.
    """
    for unit_data in default_units:
        unit = UnitOfMeasurement.query.filter_by(name=unit_data['name']).first()
        if not unit:
            unit = UnitOfMeasurement(**unit_data)
            db.session.add(unit)

    db.session.commit()

class BakedProductName(db.Model):
    """
    Represents the name of a baked product.

    Attributes:
        id (int): The unique identifier of the baked product name.
        name (str): The name of the baked product.
        user_id (int): The foreign key to the associated user who added the baked product name.

    Methods:
        __str__: Returns the string representation of the BakedProductName object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.name
    
class BakedProduct(db.Model):
    """
    Represents a baked product for sale.

    Attributes:
        id (int): The unique identifier of the baked product.
        name_id (int): The foreign key to the associated baked product name.
        quantity (Decimal): The quantity of the baked product available for sale.
        cost_price (Decimal): The cost price of the baked product.
        selling_price (Decimal): The selling price of the baked product.
        date_baked (datetime): The date the baked product was prepared.
        unit_of_measurement_id (int): The foreign key to the associated unit of measurement for the baked product.
        ingredients (list): The relationship to the BakedProductIngredient objects.
        user_id (int): The foreign key to the associated user who added the baked product.
        user (User): The relationship to the User object.

    Methods:
        __repr__: Returns a string representation of the BakedProduct object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name_id = db.Column(db.Integer, db.ForeignKey('baked_product_name.id'), nullable=False)
    quantity = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)
    cost_price = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)
    selling_price = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)
    date_baked = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'), nullable=False)
    ingredients = db.relationship('BakedProductIngredient', backref='baked_product', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('baked_products', lazy=True))

    def __repr__(self):
        return f"BakedProduct('{self.name_id}', '{self.quantity}', '{self.cost_price}', '{self.selling_price}', '{self.date_baked}')"
   
class BakedProductIngredient(db.Model):
    """
    Represents an ingredient used to bake a specific product.

    Attributes:
        id (int): The unique identifier of the baked product ingredient.
        baked_product_id (int): The foreign key to the associated baked product.
        product_id (int): The foreign key to the associated product (ingredient).
        quantity (Decimal): The quantity of the ingredient used.
        date_used (datetime): The date the ingredient was used.

    Methods:
        __repr__: Returns a string representation of the BakedProductIngredient object.
    """
    id = db.Column(db.Integer, primary_key=True)
    baked_product_id = db.Column(db.Integer, db.ForeignKey('baked_product.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.DECIMAL(precision=8, scale=2), nullable=False)  
    date_used = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"BakedProductIngredient('{self.baked_product_id}', '{self.ingredient_id}', '{self.quantity}')"
    

@login_manager.user_loader
def load_user(user_id):
    """
    Retrieve a user object by its ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        User: The User object corresponding to the given ID.
    """
    return User.query.get(int(user_id))

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    """
    Handle the 404 Not Found error.

    Args:
        error (Exception): The exception object representing the error.

    Returns:
        tuple: A tuple containing the rendered template for the 404 error page and the HTTP status code 404.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle the 500 Internal Server Error.

    Args:
        error (Exception): The exception object representing the error.

    Returns:
        tuple: A tuple containing the rendered template for the 500 error page and the HTTP status code 500.
    """
    return render_template('500.html'), 500

# Helper Functions
def get_category_name(category_id):
        """
        Retrieve the name of a category by its ID.

        Args:
            category_id (int): The ID of the category.

        Returns:
            str: The name of the category.
        """
        with app.app_context():
            user_id = current_user.id
            categories = Category.query.filter_by(user_id=user_id).all()
            category = next((cat for cat in categories if cat.id == category_id), None)
            return category.name if category else ""
        
def get_product_status(quantity):
    """
    Determine the status of a product based on its quantity.

    Args:
        quantity (float): The quantity of the product.

    Returns:
        str: The status of the product ('Out of Stock', 'Critical', 'Low', 'In Stock').
    """
    if quantity <= 0:
        return 'Out of Stock'
    elif quantity <= 5 and quantity > 0:
        return 'Critical'
    elif quantity <= 10 and quantity > 5:
        return 'Low'
    else:
        return 'In Stock'
    
def get_unit_of_measurement_name(unit_of_measurement_id):
    """
    Retrieve the name of a unit of measurement by its ID.

    Args:
        unit_of_measurement_id (int): The ID of the unit of measurement.

    Returns:
        str: The name of the unit of measurement.
    """
    with app.app_context():
        unit_of_measurement = UnitOfMeasurement.query.get(unit_of_measurement_id)
        if unit_of_measurement:
            return unit_of_measurement.name
        return ''

def get_past_week_dates():
    """
    Get the start and end dates of the past week.

    Returns:
        tuple: A tuple containing the start date and end date of the past week.
    """
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    return start_date, end_date

# Routes
@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: The rendered HTML template for the home page.
    """
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle the signup page.

    If the request method is GET, render the signup form.
    If the request method is POST, process the form data and create a new user.

    Returns:
        str: The rendered HTML template for the signup page, with the signup form or flash messages.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please choose a different one.', 'danger')
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login page.

    If the user is already authenticated, redirect to the inventory page.
    If the request method is GET, render the login form.
    If the request method is POST, process the form data and authenticate the user.

    Returns:
        str: The rendered HTML template for the login page, with the login form or flash messages.
    """
    if current_user.is_authenticated:
        flash('Welcome, Log In successful!', 'success')
        return redirect(url_for('inventory'))
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Welcome, Log In successful!', 'success')
            return redirect(next_page or url_for('inventory'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Returns:
        redirect: Redirects the user to the home page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

def get_top_ingredients(user_id, start_date, end_date):
    """
    Retrieve top ingredients used in baked products within a specific time range.

    Args:
        user_id (int): User ID.
        start_date (datetime): Start date of the time range.
        end_date (datetime): End date of the time range.

    Returns:
        list: List of top ingredients.
    """
    top_ingredient_ids = db.session.query(
        BakedProductIngredient.product_id,
        func.sum(BakedProductIngredient.quantity).label('total_quantity')
    ).join(BakedProduct).filter(
        BakedProduct.date_baked.between(start_date, end_date)
    ).group_by(BakedProductIngredient.product_id).order_by(
        func.sum(BakedProductIngredient.quantity).desc()
    ).subquery()

    top_ingredients = db.session.query(
        Product.name,
        top_ingredient_ids.c.total_quantity,
        UnitOfMeasurement.name,
        Product.quantity
    ).join(top_ingredient_ids, Product.id == top_ingredient_ids.c.product_id).join(
        UnitOfMeasurement, Product.unit_of_measurement_id == UnitOfMeasurement.id
    ).filter(
        Product.user_id == user_id
    ).all()

    return top_ingredients

def calculate_ingredient_percentages(top_ingredients):
    """
    Calculate the percentage and quantity remaining for each ingredient.

    Args:
        top_ingredients (list): List of top ingredients.

    Returns:
        list: List of top ingredients with percentage and quantity remaining.
    """
    top_ingredients_with_percentage = []
    for ingredient in top_ingredients:
        name, quantity, unit, quantity_remaining = ingredient
        percentage = round((quantity / (quantity + quantity_remaining)) * 100)
        top_ingredients_with_percentage.append((name, quantity, unit, percentage, quantity_remaining))

    return top_ingredients_with_percentage

def enumerate_top_ingredients(top_ingredients_with_percentage):
    """
    Enumerate the top ingredients with their index.

    Args:
        top_ingredients_with_percentage (list): List of top ingredients with percentage.

    Returns:
        list: List of top ingredients with index.
    """
    top_ingredients_with_index = [(index + 1, ingredient) for index, ingredient in enumerate(top_ingredients_with_percentage)]

    return top_ingredients_with_index

def get_baked_products(user_id, start_date, end_date):
    """
    Retrieve baked products baked by the user within a specific time range.

    Args:
        user_id (int): User ID.
        start_date (datetime): Start date of the time range.
        end_date (datetime): End date of the time range.

    Returns:
        list: List of baked products.
    """
    baked_products = db.session.query(
        BakedProduct,
        BakedProductName.name
    ).join(
        BakedProductName, BakedProduct.name_id == BakedProductName.id
    ).filter(
        BakedProduct.user_id == user_id,
        BakedProduct.date_baked.between(start_date, end_date)
    ).order_by(BakedProduct.date_baked).all()

    return baked_products

def format_table_data(baked_products):
    """
    Format the baked product data into a table.

    Args:
        baked_products (list): List of baked products.

    Returns:
        list: List of dictionaries containing formatted table data.
    """
    table_data = []
    for index, (baked_product, product_name) in enumerate(baked_products, start=1):
        table_data.append({
            'Index': index,
            'Baked Product Name': product_name,
            'Cost Price': baked_product.cost_price,
            'Selling Price': baked_product.selling_price,
            'Quantity Baked': baked_product.quantity,
            'Date Baked': baked_product.date_baked
        })

    return table_data


@app.route('/analytics')
@login_required
def analytics():
    """
    Display analytics data for the current user.

    Returns:
        render_template: Renders the 'analytics.html' template with the required data.
    """
    user_id = current_user.id
    
    # Calculate the start and end dates for the past 7 days
    start_date, end_date = get_past_week_dates()

    # Query top ingredients used in baked products in the past week
    top_ingredients = get_top_ingredients(user_id, start_date, end_date)

    # Calculate the percentage and quantity remaining for each ingredient
    top_ingredients_with_percentage = calculate_ingredient_percentages(top_ingredients)


    # Enumerate the top ingredients with their index
    top_ingredients_with_index = enumerate_top_ingredients(top_ingredients_with_percentage)

    # Query baked products baked in the past week
    baked_products = get_baked_products(user_id, start_date, end_date)

    # Format the baked product data into a table
    table_data = format_table_data(baked_products)

    # Get all baked products for the specific user
    baked_products = BakedProduct.query.filter_by(user_id=user_id).all()

    # Calculate the total number of unique ingredients used
    unique_ingredients = set(ingredient.product_id for product in baked_products for ingredient in product.ingredients)
    total_unique_ingredients = len(unique_ingredients)

    # Calculate the percentage of ingredients each baked product uses
    baked_product_percentages = [
        (product, len(product.ingredients), round((len(product.ingredients) / total_unique_ingredients) * 100, 2))
        for product in baked_products
    ]

    # Retrieve the names of the baked products
    baked_product_names = BakedProductName.query.filter_by(user_id=user_id).all()
    baked_product_names_dict = {name.id: name.name for name in baked_product_names}

    # Update the baked_product_percentages list to include the product names
    baked_product_percentages_with_names = [
        (baked_product_names_dict.get(product.name_id), *product_data)
        for product, *product_data in baked_product_percentages
    ]


    return render_template('analytics.html',
                           top_ingredients_with_index=top_ingredients_with_index,
                           table_data=table_data,
                           get_unit_of_measurement_name=get_unit_of_measurement_name,
                           baked_product_percentages=baked_product_percentages_with_names,
                           get_product_status=get_product_status,
                           get_category_name=get_category_name)

def get_top_ingredients(start_date, end_date, user_id):
    """
    Retrieve the top ingredients based on their quantities within a specified date range.

    Args:
        start_date (datetime): Start date.
        end_date (datetime): End date.
        user_id (int): User ID.

    Returns:
        list: List of top ingredients.
    """
    top_ingredient_ids = db.session.query(
        BakedProductIngredient.product_id,
        func.sum(BakedProductIngredient.quantity).label('total_quantity')
    ).join(BakedProduct).filter(
        BakedProduct.date_baked.between(start_date, end_date)
    ).group_by(BakedProductIngredient.product_id).order_by(
        func.sum(BakedProductIngredient.quantity).desc()
    ).limit(4).subquery()

    top_ingredients = db.session.query(
        Product.name,
        top_ingredient_ids.c.total_quantity,
        UnitOfMeasurement.name
    ).join(top_ingredient_ids, Product.id == top_ingredient_ids.c.product_id).join(
        UnitOfMeasurement, Product.unit_of_measurement_id == UnitOfMeasurement.id
    ).filter(
        Product.user_id == user_id
    ).all()

    return top_ingredients

@app.route('/inventory')
@login_required
def inventory():
    """
    Render the inventory page.

    This route is accessible to logged-in users only. It retrieves the necessary data to populate the inventory page,
    including the top ingredients used in the past 7 days, units of measurement, categories, and products owned by the user.

    Returns:
        HTML: Rendered inventory page template.
    """
    user_id = current_user.id
    units = UnitOfMeasurement.query.all()
    categories = Category.query.filter_by(user_id=user_id).all()
    products = Product.query.filter_by(user_id=user_id).all()
    
    # Calculate the start and end dates for the past 7 days
    start_date, end_date = get_past_week_dates()

    top_ingredients = get_top_ingredients(start_date, end_date, user_id)

    
    top_ingredients_with_index = [(index + 1, ingredient) for index, ingredient in enumerate(top_ingredients)]
    
    app.jinja_env.globals['get_category_name'] = get_category_name
    return render_template('inventory.html', top_ingredients_with_index=top_ingredients_with_index, categories=categories, units=units,
                           username=current_user.username, current_date=datetime.datetime.now().strftime("%d/%m/%Y"),
                           get_unit_of_measurement_name=get_unit_of_measurement_name,
                           get_product_status=get_product_status,
                           get_category_name=get_category_name, products=products)

@app.route("/create_product", methods=["POST"])
@login_required
def create_product():
    """
    Create a new product.

    This route is accessible via POST request and requires the user to be logged in.
    It expects the following JSON data in the request body:
    {
        "name": <product name>,
        "price": <product price>,
        "quantity": <product quantity>,
        "category": <category ID>,
        "description": <product description>,
        "unit_id": <unit of measurement ID>,
        "image": <image URL>
    }

    Returns:
        JSON: Response containing the created product information or an error message.
    """
    user_id = current_user.id

    # Retrieve form data
    form_data = request.json
    required_fields = ["name", "price", "quantity", "category", "description", "unit_id"]
    if not all(field in form_data for field in required_fields):
        return jsonify({"error": "Please provide all the required fields."}), 400

    try:
        new_image = Image(image_url=form_data["image"])
        db.session.add(new_image)
        db.session.commit()

        image = Image.query.filter_by(image_url=form_data["image"]).first()

        new_product = Product(
            name=form_data["name"],
            price=form_data["price"],
            quantity=form_data["quantity"],
            category_id=int(form_data["category"]),
            image_id=image.id,
            description=form_data["description"],
            user_id=user_id,
            unit_of_measurement_id=form_data["unit_id"]
        )

        unit_name = get_unit_of_measurement_name(form_data["unit_id"])
        new_category = Category.query.filter_by(id=form_data["category"], user_id=user_id).first()
        category_name = new_category.name if new_category else ""

        db.session.add(new_product)
        db.session.commit()

        status=get_product_status(form_data["quantity"])
        return jsonify({
            "message": "Product created successfully.",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "category_id": new_product.category_id,
                "quantity": new_product.quantity,
                "category": category_name,
                "unit": unit_name,
                "status": status
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/category', methods=['POST'])
@login_required
def create_category():
    """
    Create a new category.

    This route is accessible via a POST request and is only available to logged-in users. It creates a new category
    based on the provided category name in the request body.

    Returns:
        JSON: The newly created category data if successful, or an error message if an exception occurs.
    """
    user_id = current_user.id
    category_name = request.json['category']
    new_category = Category(name=category_name, user_id=user_id)

    try:
        db.session.add(new_category)
        db.session.commit()
        category_data = {
            'id': new_category.id,
            'name': new_category.name,
            'user_id': new_category.user_id
        }
        return jsonify(category_data), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@app.route('/product_details', methods=['GET', 'PUT'])
@login_required
def product_details():
    """
    Get or update the details of a product.

    This route is accessible via GET and PUT requests and is only available to logged-in users. It retrieves the details
    of a specific product or updates the details of a product based on the request method.

    Returns:
        If the method is GET:
            - HTML template with the product details if the product exists.
            - HTML template for a 404 error if the product does not exist.
        If the method is PUT:
            - JSON with the updated product details if the product and image exist.
            - HTML template for a 404 error if the image does not exist.
    """
    user_id = current_user.id  
    if request.method == 'GET':
        id = request.args.get('id')
        product = Product.query.filter_by(id=id, user_id=user_id).first()
        if product:
            image = Image.query.filter_by(id=product.image_id).first()
            categories = Category.query.filter_by(user_id=user_id).all()
            category = Category.query.filter_by(id=product.category_id, user_id=user_id).first()
            category_name = category.name if category else None
            category_id = category.id
            
            product_details = {
                'name': product.name,
                'id': product.id,
                'price': product.price,
                'description': product.description,
                'quantity': product.quantity,
                'category_name': category_name,
                'category_id': category_id,
                'user_id': product.user_id,
                'image_url': image.image_url,
                'url_id': image.id,
                'categories': categories
            }
            return render_template('product_details.html', product=product_details)
        else:
            return render_template('404.html'), 404
        
    elif request.method == 'PUT':
        form_data = request.json
        required_fields = ["name", "price", "quantity", "category", "description"]

        if not all(field in form_data for field in required_fields):
            return jsonify({"error": "Please provide all the required fields."}), 400
        
        product = Product.query.filter_by(id=form_data["productId"], user_id=user_id).first()
        image = Image.query.filter_by(id=form_data["urlId"]).first()

        if image:
            image.image_url = form_data["image"]
            # Commit the changes to the database
            db.session.commit()
        else:
            return render_template('404.html'), 404

        if product:
            # Update the product information with the new data
            product.name = form_data["name"]
            product.price = form_data["price"]
            product.quantity = form_data["quantity"]
            product.category_id = form_data["category"]
            product.description = form_data["description"]
            product.image_id = form_data["urlId"]
            # Commit the changes to the database
            db.session.commit()
        else:
            return render_template('404.html'), 404

        # query the new product
        new_product = Product.query.filter_by(id=form_data
        ["productId"], user_id=user_id).first()

        # query category
        new_category = Category.query.filter_by(id=form_data["category"], user_id=user_id).first()
        categories = Category.query.filter_by(user_id=user_id).all()
        return jsonify({
                'name': new_product.name,
                'product_id': new_product.id,
                'price': new_product.price,
                'description': new_product.description,
                'quantity': new_product.quantity,
                'category_name': new_category.name,
                'category_id': new_product.category_id,
                'user_id': new_product.user_id,
                'image_url': form_data["image"],
                'url_id': new_product.image_id,
                #'categories ': categories 
        }), 200

@app.route('/category_products', methods=['POST'])
@login_required
def category_products():
    """
    Get the products belonging to a specific category.

    This route is accessible via POST request and is only available to logged-in users. It retrieves the products that
    belong to a specific category based on the provided category ID.

    Returns:
        - JSON with the product data if the category ID is valid.
        - JSON with an error message if the category ID is missing.
    """
    category_id = request.json['id']

    if category_id is None:
        return jsonify({'error': 'Category ID is missing'}), 400

    user_id = current_user.id
    if category_id == -1:
        products = Product.query.filter_by(user_id=user_id).all()
    else:
        products = Product.query.filter_by(category_id=category_id, user_id=user_id).all()


    product_data = []
    for product in products:

        product_info = {
            'index': products.index(product) + 1,
            'id': product.id,
            'name': product.name,
            'category': get_category_name(product.category_id),
            'quantity': product.quantity,
            'status': get_product_status(product.quantity),
            'unit': get_unit_of_measurement_name(product.unit_of_measurement_id)
        }
        product_data.append(product_info)

    return jsonify(product_data), 200


@app.route('/bake', methods=['GET', 'POST'])
@login_required
def bake():
    """
    Create a baked product.

    This route is accessible via GET and POST requests and is only available to logged-in users. 
    If accessed via GET, it retrieves the necessary data for baking a product, such as the available baked product names
    and units of measurement, and renders the 'bake.html' template with the retrieved data.
    If accessed via POST, it creates a baked product based on the provided data.

    Returns:
        - If accessed via GET, renders the 'bake.html' template with the necessary data.
        - If accessed via POST and the baked product is successfully created, returns a JSON response with a success message.
        - If accessed via POST and any error occurs during the creation of the baked product, returns a JSON response with an error message.
    """
    user_id = current_user.id
    if request.method == 'GET':
        baked_products = BakedProductName.query.filter_by(user_id=user_id).all()
        units = UnitOfMeasurement.query.all()
        return render_template('bake.html', units = units, baked_products=baked_products)
    else:
        data = request.get_json()
        name_id = data.get('name_id')
        quantity = data.get('quantity')
        totalPrice = data.get('totalPrice')
        unit_id = data.get('unit')
        ingredients = data.get('ingredients')
        selling_price = data.get('selling_price')

        # Check ingredient availability
        for ingredient in ingredients:
            product_id = ingredient.get('id')
            product_quantity = ingredient.get('quantity')

            product = Product.query.get(product_id)

            if product is None:
                return jsonify({"error": f"Product with ID {product_id} not found."}), 404

            if product.quantity < product_quantity:
                return jsonify({"error": f"Insufficient quantity for product {product.name}."}), 400

        # Create baked product
        cost_price = Decimal(totalPrice)
        user = User.query.get(user_id)
        baked_product = BakedProduct(name_id=name_id, quantity=quantity, cost_price=cost_price, unit_of_measurement_id=unit_id, user=user, selling_price=Decimal(selling_price))

        db.session.add(baked_product)
        db.session.flush()

        # Add ingredients to baked product
        for ingredient in ingredients:
            product_id = ingredient.get('id')
            product_quantity = ingredient.get('quantity')

            baked_product_ingredient = BakedProductIngredient(
                baked_product_id=baked_product.id,
                product_id=product_id,
                quantity=product_quantity,
            )
            db.session.add(baked_product_ingredient)

            # Update product quantity
            product_quantity = Decimal(product_quantity)
            product = Product.query.get(product_id)
            product.quantity -= product_quantity
            db.session.add(product)

        db.session.commit()

        return jsonify({
            "message": "Baked product created successfully.",
            "selling_price": selling_price 
            }), 200
    

@app.route('/ingredients/search')
@login_required
def search_ingredients():
    """
    Search for ingredients based on a given search term.

    This route is accessible only to logged-in users and is used to search for ingredients 
    based on a provided search term. The search is case-insensitive and returns ingredients 
    that match the search term, along with their IDs, labels, values, and prices, in a JSON response.

    Returns:
        - A JSON response containing a list of ingredients that match the search term.
          Each ingredient object in the response includes its ID, label, value, and price.
    """
    search_term = request.args.get('term', '')

    ingredients = Product.query.filter(
    Product.name.ilike(f'%{search_term}%'), Product.user_id == current_user.id).all()
    response = [{'id': ingredient.id, 'label': ingredient.name, 'value': ingredient.name, 'price': ingredient.price} for ingredient in ingredients]

    return jsonify(response)
        

@app.route('/delete_product/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    """
    Delete a product.

    This route is accessible only to logged-in users. It allows the deletion of a product
    with the specified ID. The product is retrieved from the database based on the provided ID.
    If the product is found and the current user is the owner of the product or an admin user,
    the product is deleted from the database. Otherwise, an error message is returned.

    Args:
        - id (int): The ID of the product to be deleted.

    Returns:
        - A JSON response containing a success message if the product is deleted successfully.
          If the product is not found or the deletion fails, an error message is returned.
    """
    product = Product.query.get_or_404(id)

    # Check if the current user is the owner of the product
    if product.user_id != current_user.id and not current_user.is_admin:
        return jsonify(error='Unauthorized'), 403

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify(message='Product deleted successfully')
    except:
        return jsonify(error='Failed to delete the product'), 500
  

from titlecase import titlecase

@app.route('/create_baked_product', methods=['POST'])
@login_required
def create_baked_product():
    if request.method == 'POST':
        try:
            user_id = current_user.id
            name = request.form.get('name')

            # Clean the name by removing trailing spaces and convert to title case
            cleaned_name = titlecase(name.strip())

            # Check if the user has already created the product
            existing_product = BakedProductName.query.filter_by(name=cleaned_name, user_id=user_id).first()
            if existing_product:
                return jsonify({'error': 'You have already created this baked product.'})

            # Create a new BakedProductName instance
            product_name = BakedProductName(name=cleaned_name, user_id=user_id)
            db.session.add(product_name)
            db.session.commit()

            # Prepare the response JSON with the product details
            response = {
                'message': 'Baked product created successfully.',
                'product': {
                    'name': product_name.name,
                    'id': product_name.id
                }
            }

            return jsonify(response)
        except Exception as e:
            # Handle the specific exception or provide a generic error message
            return jsonify({'error': 'Failed to create baked product. Please try again.'})





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_unit_of_measurement()
    app.run(debug=True)

