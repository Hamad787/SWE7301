from flask_restx import Resource, fields
from flask import request
from models.payment import Payment
from schemas.payment_schema import PaymentSchema
from models.order import Order
from extensions import db
from app import api
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

# Define the payment request model for Swagger documentation
payment_model = api.model('Payment', {
    'amount': fields.Float(required=True, description='Amount of the payment'),
    'payment_method': fields.String(required=True, description='Method of payment (e.g., Credit Card, PayPal)')
})

# Define the response model for Swagger documentation (successful payment response)
payment_response_model = api.model('PaymentResponse', {
    'id': fields.Integer(dump_only=True, description='Payment ID'),
    'amount': fields.Float(description='Amount of the payment'),
    'payment_method': fields.String(description='Method of payment'),
    'order_id': fields.Integer(description='ID of the associated order')
})

class PaymentView(Resource):
    @jwt_required()
    @api.doc('create_payment')  
    @api.expect(payment_model)  
    @api.marshal_with(payment_response_model, code=201)  
    def post(self, order_id):
        """POST /api/order/<order_id>/payment"""
        """Create a payment for an order"""
        order = Order.query.get(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        
        data = request.get_json()
        payment_schema = PaymentSchema()
        try:
            # Deserialize incoming data and create Payment instance
            payment_data = payment_schema.load(data)
            payment = Payment(**payment_data)
            db.session.add(payment)
            db.session.commit()
            return payment_schema.dump(payment), 201
        except ValidationError as err:
            return err.messages, 400
