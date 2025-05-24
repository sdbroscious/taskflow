from app import create_app, db
import os

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Delete the database file if it exists
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'taskflow.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    # Initialize the database
    init_db()
