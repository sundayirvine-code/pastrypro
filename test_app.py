import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, User, Product, Category, Image

class AppTestCase(TestCase):
    def create_app(self):
        app.config.from_object('test_config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertTemplateUsed('index.html')

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assert200(response)
        self.assertTemplateUsed('signup.html')

        # Test form submission with valid data
        response = self.client.post('/signup', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('login.html')
        # Assert that the user is created in the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

        # Test form submission with invalid data
        response = self.client.post('/signup', data={
            'username': '',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('signup.html')
        # Assert that the user is not created in the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNone(user)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assert200(response)
        self.assertTemplateUsed('login.html')

        # Test form submission with valid credentials
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('inventory.html')

        # Test form submission with invalid credentials
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('login.html')
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout_route(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed('index.html')

    def test_inventory_route(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # Login as the test user
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        response = self.client.get('/inventory')
        self.assert200(response)
        self.assertTemplateUsed('inventory.html')

    def test_create_product_route(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # Login as the test user
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        # Create a test category
        category = Category(name='Test Category', user_id=user.id)
        db.session.add(category)
        db.session.commit()

        # Test form submission with valid data
        response = self.client.post('/create_product', json={
            'name': 'Test Product',
            'price': 9.99,
            'quantity': 10,
            'category': category.id,
            'image': 'https://example.com/image.jpg',
            'description': 'Test product description'
        }, follow_redirects=True)
        self.assert200(response)
        data = response.get_json()
        self.assertEqual(data['message'], 'Product created successfully.')
        self.assertEqual(data['product']['name'], 'Test Product')

    def test_create_category_route(self):
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # Login as the test user
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        # Test form submission with valid data
        response = self.client.post('/category', json={'category': 'Test Category'}, follow_redirects=True)
        self.assert200(response)
        data = response.get_json()
        self.assertEqual(data['name'], 'Test Category')
        self.assertEqual(data['user_id'], user.id)

if __name__ == '__main__':
    unittest.main()
