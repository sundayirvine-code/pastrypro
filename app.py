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
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            session['email'] = user.email
            return redirect(url_for('inventory'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('home'))


def get_category_name(category_id):
        with app.app_context():
            user = User.query.filter_by(username=session.get('username')).first()
            categories = Category.query.filter_by(user_id=user.id).all()
            category = next((cat for cat in categories if cat.id == category_id), None)
            return category.name if category else ""

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

@app.route('/product_details', methods=['GET'])
@login_required
def product_details():
    name = request.args.get('name')
    id = request.args.get('id')
    user = User.query.filter_by(username=session.get('username')).first()
    categories = Category.query.filter_by(user_id=user.id).all()
    product = Product.query.filter_by(name=name, id=id, user_id=user.id).first()

    if product:
        category = Category.query.filter_by(id=product.category_id, user_id=user.id).first()
        category_name = category.name if category else None
        category_id = category.id
        image = Image.query.filter_by(id=product.image_id).first()
        
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
            'categories': categories
        }
        return render_template('product_details.html', product=product_details)
    else:
        return render_template('404.html'), 404











if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
