# TaskFlow - A Todoist Clone

TaskFlow is a simple task management application inspired by Todoist, built with Python (Flask) and Tailwind CSS. It was build using Cascade, an AI-powered code generator that lives in the Windsurf IDE.

## Features

- User authentication (login/register)
- Create, read, update, and delete tasks
- Organize tasks into projects
- Set task priorities and due dates
- Clean, responsive UI with Tailwind CSS

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd taskflow
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Set the Flask application:
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development  # For development mode
   ```
   (On Windows, use `set` instead of `export`)

## Running the Application

1. Initialize the database:
   ```bash
   flask db upgrade
   python init_db.py  # Optional: adds sample data
   ```

2. Start the development server:
   ```bash
   flask run
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Running Tests

1. Install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

3. Run with coverage report:
   ```bash
   pytest --cov=app tests/
   ```

## Project Structure

```
taskflow/
├── app/                  # Application package
│   ├── __init__.py      # App initialization
│   ├── auth/            # Authentication blueprint
│   ├── main/            # Main blueprint (tasks, projects)
│   ├── models.py        # Database models
│   ├── static/          # Static files (CSS, JS)
│   └── templates/       # Jinja2 templates
├── migrations/          # Database migrations
├── instance/            # Instance-specific config
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures and configuration
│   ├── factories.py     # Factory Boy model factories
│   ├── main/            # Tests for main blueprint
│   │   └── test_views.py # View function tests
│   └── test_models.py   # Model tests
├── .flaskenv            # Flask environment variables
├── requirements.txt     # Project dependencies
├── requirements-test.txt # Test dependencies
├── pytest.ini          # Pytest configuration
└── run.py               # Application entry point
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask
- SQLAlchemy
- Tailwind CSS
- Font Awesome
- Todoist for inspiration
