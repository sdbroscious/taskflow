#!/usr/bin/env python3
"""
TaskFlow - A simple task management application.
"""
import os
from app import create_app, db
from app.models import Task  # Removed User and Project models

def create_db_tables():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()

def run_app():
    """Run the Flask development server."""
    # Set up the application
    app = create_app()
    
    # Create database tables
    with app.app_context():
        create_db_tables()
    
    # Run the application
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_RUN_PORT', 8080))  # Using port 8080 to avoid conflicts with macOS AirPlay
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() in ('true', '1', 't')
    
    app.run(host=host, port=port, debug=debug)

# Create the app instance for shell context
app = create_app()

# Shell context for Flask shell command
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Task': Task,
    }

if __name__ == '__main__':
    run_app()
