from flask import Flask
from extensions import db, jwt, migrate
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and initialize API after app creation
    from api import api
    api.init_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
