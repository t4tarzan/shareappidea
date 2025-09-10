from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
               template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
               static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
    
    # Configure logging
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Ensure log directory exists
        log_dir = os.path.join(app.root_path, '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'app.log'),
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Startup Ideas startup')
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    
    # Ensure instance folder exists
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    
    # Set up database
    db_path = os.path.join(app.root_path, '..', 'instance', 'startup_ideas.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Make newsletter form available to all templates
    @app.context_processor
    def inject_newsletter_form():
        from .forms import NewsletterSignupForm
        return dict(newsletter_form=NewsletterSignupForm())
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
