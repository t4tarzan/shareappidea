from app import db
from sqlalchemy import text

def apply_migration():
    with db.engine.begin() as connection:
        # Check if the column already exists
        result = connection.execute(
            text("PRAGMA table_info(idea)")
        )
        columns = [row[1] for row in result]
        
        if 'featured' not in columns:
            print("Adding 'featured' column to 'idea' table...")
            try:
                # Add the featured column
                connection.execute(
                    text("""
                    ALTER TABLE idea 
                    ADD COLUMN featured BOOLEAN NOT NULL DEFAULT 0
                    """)
                )
                print("Successfully added 'featured' column.")
                
                # Add an index for better performance
                connection.execute(
                    text("CREATE INDEX IF NOT EXISTS idx_idea_featured ON idea (featured)")
                )
                print("Created index on 'featured' column.")
                print("Migration completed successfully!")
                
            except Exception as e:
                print(f"Error applying migration: {e}")
                raise
        else:
            print("'featured' column already exists in 'idea' table.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        apply_migration()
