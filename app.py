# app.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import datetime
from flask_login import LoginManager, login_required, current_user, UserMixin



app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#models
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
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    # Define other product fields as needed
    
    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def __repr__(self):
        return f"Category('{self.name}')"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Image('{self.image_url}')"
    
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

# Define your routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user based on form data
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Redirect to a success page or login page
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists and password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Store the user information in the session
            session['username'] = user.username
            session['email'] = user.email
            # Redirect to a logged-in page or dashboard
            return redirect(url_for('inventory'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Clear the user information from the session
    session.pop('username', None)
    session.pop('email', None)
    # Redirect to the login page or any other desired page
    return redirect(url_for('home'))


@app.route('/inventory')
@login_required
def inventory():
    # Get the currently logged-in user
    user = User.query.filter_by(username=session.get('username')).first()
    
    # Fetch only the products associated with the user from the database
    products = Product.query.filter_by(user_id=user.id).all()

    # Fetch only the categories associated with the user from the database
    categories = Category.query.filter_by(user_id=user.id).all()

    # Access the 'username' from the session
    username = session.get('username')
    email = session.get('email')
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    return render_template('inventory.html', products=products, categories = categories,username=username, current_date=current_date)
    
@app.route("/create_product", methods=["POST"])
@login_required
def create_product():
    # Get the form data from the AJAX request
    form_data = request.json

    # Perform validation on the form data (you can add your own validation logic here)
    if not form_data.get("name") or not form_data.get("price") or not form_data.get("quantity") or not form_data.get("category") or not form_data.get("description"):
        return jsonify({"error": "Please provide all the required fields."}), 400

    # create image
    new_image = Image(image_url=form_data["image"])
    # Add the new image to the database session
    db.session.add(new_image)
    db.session.commit()

    # Get the currently logged-in user
    user = User.query.filter_by(username=session.get('username')).first()

    image = Image.query.filter_by(image_url=form_data["image"]).first()

    # Create a new Product object
    new_product = Product(
        name=form_data["name"],
        price=form_data["price"],
        quantity=form_data["quantity"],
        category_id=form_data["category"],
        image_id=image.id,
        description=form_data["description"],
        user_id=user.id 
    )

    # Add the new product to the database session
    db.session.add(new_product)
    db.session.commit()

    # Return a response indicating success
    return jsonify({"message": "Product created successfully."}), 200


@app.route('/category', methods=['POST'])
@login_required
def create_category():
    category_name = request.json['category']

    # Get the currently logged-in user
    user = User.query.filter_by(username=session.get('username')).first()

    # Create a new Category object associated with the user
    new_category = Category(name=category_name, user_id=user.id)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.name), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()


if __name__ == '__main__':
    with app.app_context():
        #create tables
        db.create_all()
    app.run(debug=True)










