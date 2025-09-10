from app import create_app, db
from app.models import NewsletterSubscriber
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # This will create all database tables
    db.create_all()
    print("Database tables created successfully.")
    
    # Verify the newsletter_subscribers table was created
    inspector = inspect(db.engine)
    if 'newsletter_subscribers' in inspector.get_table_names():
        print("✅ newsletter_subscribers table exists.")
    else:
        print("❌ Error: newsletter_subscribers table was not created.")
    
    # Print all tables for verification
    print("\nCurrent database tables:")
    for table in inspector.get_table_names():
        print(f"- {table}")
