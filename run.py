#!/usr/bin/env python3
import os
import sys
from app import create_app, db
from app.models import Idea

def init_db(app):
    with app.app_context():
        db.create_all()
        print("Database tables created!")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('instance', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
    # Create app and initialize database
    app = create_app()
    init_db(app)
    
    # Run the app
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8083
    app.run(debug=True, host='0.0.0.0', port=port)
