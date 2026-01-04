from flask import Flask
from models import db
from routes import main
from config import DevelopmentConfig # Import your config class

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    
    # Load configuration from the class
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()