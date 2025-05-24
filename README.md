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

1. Start the development server:
   ```bash
   flask run
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
taskflow/
├── app/
│   ├── __init__.py         # Application factory
│   ├── models.py           # Database models
│   ├── auth/               # Authentication blueprint
│   │   ├── __init__.py
│   │   └── forms.py
│   ├── main/               # Main application blueprint
│   │   ├── __init__.py
│   │   └── forms.py
│   ├── static/             # Static files (CSS, JS, images)
│   │   ├── css/
│   │   └── js/
│   └── templates/          # HTML templates
│       ├── auth/
│       ├── base.html
│       └── main/
├── migrations/             # Database migrations
├── config.py               # Configuration
├── requirements.txt        # Dependencies
└── run.py                  # Application entry point
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
