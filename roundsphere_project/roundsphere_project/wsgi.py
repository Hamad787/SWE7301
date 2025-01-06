import os
from flask import Flask
from django.core.wsgi import get_wsgi_application
from waitress import serve

# Set up the Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roundsphere_project.settings')

# Initialize the Django application
django_app = get_wsgi_application()

# Initialize Flask application
flask_app = Flask(__name__)

# Define Flask route(s)
@flask_app.route('/flask/data')
def flask_data():
    return {"message": "This is data from Flask API"}

# Define the WSGI application to route requests to Flask or Django based on URL
def application(environ, start_response):
    # Check if the request is for Flask API
    if environ['PATH_INFO'].startswith('/flask/'):
        environ['PATH_INFO'] = environ['PATH_INFO'][6:]  # Strip '/flask' from the path
        return flask_app(environ, start_response)
    
    # Otherwise, route the request to Django
    return django_app(environ, start_response)

# Use Waitress to serve the application (or Gunicorn for production)
if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=5000)
