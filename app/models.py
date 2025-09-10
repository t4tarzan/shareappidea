from datetime import datetime
from . import db
from sqlalchemy.sql import func

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    problem = db.Column(db.Text, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    featured = db.Column(db.Boolean, default=False, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    
    def __repr__(self):
        return f"<Idea '{self.title}'>"


class NewsletterSubscriber(db.Model):
    """Model for newsletter subscribers"""
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, server_default=func.now())
    unsubscribed_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, email, name=None):
        self.email = email
        self.name = name
        self.is_active = True
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'
