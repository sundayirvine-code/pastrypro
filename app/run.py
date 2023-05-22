# run.py

from flask import Flask
from config import Config
from routes import bp as routes_bp

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(routes_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
