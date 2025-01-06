# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

# Add JWT claims loader
@jwt.user_identity_loader
def user_identity_lookup(identity):
    # Always convert identity to string
    return str(identity)

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
        'sub': str(identity),  # Ensure subject is always a string
        'type': 'access'
    }
