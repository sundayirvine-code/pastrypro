from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import datetime
from flask_login import LoginManager, login_required, current_user, UserMixin, login_user, logout_user

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '\xce!\x9e\x04\x00\x03\xdf\x88\xf1\x1b@m\xe2\xc6R\xd80\xf6H\x84\xe0e\xc1\x02'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(UserMixin, db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'), nullable=False)
    unit_of_measurement = db.relationship('UnitOfMeasurement')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __repr__(self):
        return f"Category('{self.name}')"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Image('{self.image_url}')"


class UnitOfMeasurement(db.Model):
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
    for unit_data in default_units:
        unit = UnitOfMeasurement.query.filter_by(name=unit_data['name']).first()
        if not unit:
            unit = UnitOfMeasurement(**unit_data)
            db.session.add(unit)

    db.session.commit()

# Seed the UnitOfMeasurement table
with app.app_context():
    seed_unit_of_measurement()

class BakedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date_baked = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ingredients = db.relationship('BakedProductIngredient', backref='baked_product', lazy=True)

    def __repr__(self):
        return f"BakedProduct('{self.name}', '{self.quantity}', '{self.total_price}', '{self.date_baked}')"
    

class BakedProductIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baked_product_id = db.Column(db.Integer, db.ForeignKey('baked_product.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_used = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"BakedProductIngredient('{self.baked_product_id}', '{self.ingredient_id}', '{self.quantity}')"
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inventory')) 
    form = LoginForm()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('inventory'))
            else:
                flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def get_category_name(category_id):
        with app.app_context():
            user = User.query.filter_by(username=session.get('username')).first()
            categories = Category.query.filter_by(user_id=user.id).all()
            category = next((cat for cat in categories if cat.id == category_id), None)
            return category.name if category else ""
        
def get_product_status(quantity):
    if quantity <= 0:
        return 'Out of Stock'
    elif quantity <= 5 and quantity > 0:
        return 'Critical'
    elif quantity <= 10 and quantity > 5:
        return 'Low'
    else:
        return 'In Stock'


@app.route('/inventory')
@login_required
def inventory():
    user = User.query.filter_by(username=session.get('username')).first()
    products = Product.query.filter_by(user_id=user.id).all()
    categories = Category.query.filter_by(user_id=user.id).all()
    app.jinja_env.globals['get_category_name'] = get_category_name
    return render_template('inventory.html', products=products, categories=categories,
                           username=session.get('username'), current_date=datetime.datetime.now().strftime("%d/%m/%Y"))

@app.route("/create_product", methods=["POST"])
@login_required
def create_product():
    form_data = request.json
    required_fields = ["name", "price", "quantity", "category", "description"]
    if not all(field in form_data for field in required_fields):
        return jsonify({"error": "Please provide all the required fields."}), 400

    new_image = Image(image_url=form_data["image"])
    db.session.add(new_image)
    db.session.commit()

    user = User.query.filter_by(username=session.get('username')).first()
    image = Image.query.filter_by(image_url=form_data["image"]).first()

    new_product = Product(
        name=form_data["name"],
        price=form_data["price"],
        quantity=form_data["quantity"],
        category_id=form_data["category"],
        image_id=image.id,
        description=form_data["description"],
        user_id=user.id 
    )

    new_category = Category.query.filter_by(id=form_data["category"], user_id=user.id).first()
    category_name = new_category.name if new_category else ""

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully.",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "category_id": new_product.category_id,
            "quantity": new_product.quantity,
            "category": category_name
        }
    }), 200

@app.route('/category', methods=['POST'])
@login_required
def create_category():
    category_name = request.json['category']
    user = User.query.filter_by(username=session.get('username')).first()
    new_category = Category(name=category_name, user_id=user.id)

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
    user = User.query.filter_by(username=session.get('username')).first()
    if request.method == 'GET':
        id = request.args.get('id')
        product = Product.query.filter_by(id=id, user_id=user.id).first()
        if product:
            image = Image.query.filter_by(id=product.image_id).first()
            categories = Category.query.filter_by(user_id=user.id).all()
            category = Category.query.filter_by(id=product.category_id, user_id=user.id).first()
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
        
        product = Product.query.filter_by(id=form_data["productId"], user_id=user.id).first()
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
        ["productId"], user_id=user.id).first()

        # query category
        new_category = Category.query.filter_by(id=form_data["category"], user_id=user.id).first()
        categories = Category.query.filter_by(user_id=user.id).all()
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
    category_id = request.json['id']

    if category_id is None:
        return jsonify({'error': 'Category ID is missing'}), 400

    user = User.query.filter_by(username=session.get('username')).first()
    if category_id == -1:
        products = Product.query.filter_by(user_id=user.id).all()
    else:
        products = Product.query.filter_by(category_id=category_id, user_id=user.id).all()


    product_data = []
    for product in products:
        product_info = {
            'index': products.index(product) + 1,
            'id': product.id,
            'name': product.name,
            'category': get_category_name(product.category_id),
            'quantity': product.quantity,
            'status': get_product_status(product.quantity)
        }
        product_data.append(product_info)

    return jsonify(product_data), 200


@app.route('/bake', methods=['GET', 'POST'])
@login_required
def bake():
    if request.method == 'GET':
        return render_template('bake.html')
    else:
        data = request.get_json()
        pastry_name = data.get('name')
        quantity = data.get('quantity')
        ingredients = data.get('ingredients')
        totalPrice = data.get('totalPrice')
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
        baked_product = BakedProduct(name=pastry_name, quantity=quantity, total_price=totalPrice)
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
            product = Product.query.get(product_id)
            product.quantity -= product_quantity
            db.session.add(product)

        db.session.commit()

        return jsonify({"message": "Baked product created successfully."}), 200
    

@app.route('/ingredients/search')
@login_required
def search_ingredients():
    search_term = request.args.get('term', '')

    ingredients = Product.query.filter(Product.name.ilike(f'%{search_term}%')).all()
    response = [{'id': ingredient.id, 'label': ingredient.name, 'value': ingredient.name, 'price': ingredient.price} for ingredient in ingredients]

    return jsonify(response)
        
        
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
