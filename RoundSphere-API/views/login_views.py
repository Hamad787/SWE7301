from flask_restx import Resource, fields
from flask import request
from api import ns_auth as api
from models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

# Define the login request model for Swagger documentation
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username', example='john_doe'),
    'password': fields.String(required=True, description='Password', example='password123')
})

# Define the response model for Swagger documentation
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token')
})

@api.route('/login')
class LoginView(Resource):
    @api.doc('login',
             description='Login to get access token',
             responses={200: 'Login successful', 401: 'Invalid credentials'})
    @api.expect(login_model)
    @api.marshal_with(token_model)
    def post(self):
        """Login endpoint"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(username))  # Use username as string identity
            refresh_token = create_refresh_token(identity=str(username))  # Use username as string identity
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        api.abort(401, "Invalid username or password")
