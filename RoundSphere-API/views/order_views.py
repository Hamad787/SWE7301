from flask_restx import Resource, fields
from flask import request
from models.order import Order
from schemas.order_schema import OrderSchema
from extensions import db
from app import api
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

# Define the request model for Swagger documentation (input for POST requests)
order_model = api.model('Order', {
    'customer_name': fields.String(required=True, description='Customer name'),
    'product_id': fields.Integer(required=True, description='Product ID for the order'),
    'quantity': fields.Integer(required=True, description='Quantity ordered'),
    'total_price': fields.Float(required=True, description='Total price of the order')
})

# Define the response model for Swagger documentation (response for GET and POST)
order_response_model = api.model('OrderResponse', {
    'id': fields.Integer(dump_only=True, description='Order ID'),
    'customer_name': fields.String(description='Customer name'),
    'product_id': fields.Integer(description='Product ID for the order'),
    'quantity': fields.Integer(description='Quantity ordered'),
    'total_price': fields.Float(description='Total price of the order')
})

class OrderViewSet(Resource):
    @jwt_required()
    @api.doc('get_all_orders')  # Swagger route description for GET /api/orders
    @api.marshal_with(order_response_model, code=200)  # Define the response model for GET
    def get(self, order_id=None):
        """GET /api/orders/ or /api/orders/<order_id>"""
        if order_id:
            order = Order.query.get(order_id)
            if order:
                return OrderSchema().dump(order), 200
            return {'message': 'Order not found'}, 404
        else:
            orders = Order.query.all()
            return OrderSchema(many=True).dump(orders), 200

    @jwt_required()
    @api.doc('create_order')  # Swagger route description for POST /api/orders
    @api.expect(order_model)  # Expect input in the format of the order_model
    @api.marshal_with(order_response_model, code=201)  # Define the response model for POST
    def post(self):
        """POST /api/orders/"""
        data = request.get_json()
        order_schema = OrderSchema()
        try:
            # Deserialize incoming data and create Order instance
            order_data = order_schema.load(data)
            order = Order(**order_data)
            db.session.add(order)
            db.session.commit()
            return order_schema.dump(order), 201
        except ValidationError as err:
            return err.messages, 400
