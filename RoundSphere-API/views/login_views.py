from flask_restx import Resource, fields
from flask import request
from app import api
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

# Define the login request model for Swagger documentation
login_model = api.model('Login', {
    'username': fields.String(required=True, description='The username for login'),
    'password': fields.String(required=True, description='The password for login')
})

# Define the response model for Swagger documentation
login_response_model = api.model('LoginResponse', {
    'access_token': fields.String(description='JWT Access Token')
})

class LoginView(Resource):
    @api.doc('login_user')  # Swagger route description
    @api.expect(login_model)  # Expect input in the format of the login_model
    @api.marshal_with(login_response_model, code=200)  # Specify the response format for successful login
    def post(self):
        """POST /api/login/"""
        # Retrieve username and password from the request
        username = request.json.get('username')
        password = request.json.get('password')

        # In a real application, you'd validate these credentials (e.g., using hashed passwords)
        if username == "admin" and password == "admin":
            # Generate the access token using the JWT Manager
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401
