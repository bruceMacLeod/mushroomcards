from setuptools import setup, find_packages

setup(
    name="mushroom-flashcards",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.1.0",
        "flask-cors==5.0.0",
        "python-dotenv==1.0.1",
        "pandas==1.5.3",
        "google-generativeai==0.8.4",
        "requests==2.32.3",
        "werkzeug==3.1.3",
        "gunicorn==23.0.0",
    ],
)