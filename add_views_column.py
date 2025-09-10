from app import db
from sqlalchemy import text

def add_views_column():
    with db.engine.begin() as connection:
        # Check if the views column already exists
        result = connection.execute(
            text("PRAGMA table_info(idea)")
        )
        columns = [row[1] for row in result]
        
        if 'views' not in columns:
            print("Adding 'views' column to 'idea' table...")
            try:
                # Add the views column with default value 0
                connection.execute(
                    text("""
                    ALTER TABLE idea 
                    ADD COLUMN views INTEGER NOT NULL DEFAULT 0
                    """)
                )
                print("Successfully added 'views' column.")
                
                # Add an index for better performance on views queries
                connection.execute(
                    text("CREATE INDEX IF NOT EXISTS idx_idea_views ON idea (views)")
                )
                print("Created index on 'views' column.")
                
            except Exception as e:
                print(f"Error applying migration: {e}")
                raise
        else:
            print("'views' column already exists in 'idea' table.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        add_views_column()
