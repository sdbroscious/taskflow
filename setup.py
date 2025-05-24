from setuptools import setup, find_packages

setup(
    name="taskflow",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.3.3',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-Login==0.6.2',
        'Flask-Migrate==3.1.0',
        'python-dotenv==1.0.0',
        'Werkzeug==2.3.7',
        'email-validator==2.0.0',
        'Flask-WTF==1.2.1',
        'SQLAlchemy==1.4.46',
        'alembic==1.8.1'
    ],
)
