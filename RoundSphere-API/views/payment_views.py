from flask_restx import Resource, fields
from flask import request
from api import ns_payment as api
from models.payment import Payment
from schemas.payment_schema import PaymentSchema
from extensions import db
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from models.order import Order

payment_model = api.model('Payment', {
    'order_id': fields.Integer(required=True, description='Order ID', example=1),
    'amount': fields.Float(required=True, description='Payment amount', example=119.99),
    'payment_method': fields.String(required=True, description='Payment method',
                                  enum=['credit_card', 'debit_card', 'paypal'],
                                  example='paypal'),
    'payment_details': fields.Raw(required=True, description='Payment details',
                                example={
                                    'payment_id': '123',
                                    'status': 'completed'
                                })
})

payment_response_model = api.inherit('PaymentResponse', {
    'id': fields.Integer(description='Payment ID'),
    'order_id': fields.Integer(description='Order ID'),
    'amount_paid': fields.Float(description='Amount paid'),
    'payment_method': fields.String(description='Payment method'),
    'payment_date': fields.DateTime(description='Payment date'),
    'payment_id': fields.String(description='Payment ID from provider'),
    'status': fields.String(description='Payment status')
})

@api.route('/order/<int:order_id>')
@api.param('order_id', 'The order identifier')
class PaymentView(Resource):
    @api.doc('get_payment_status',
             description='Get payment status for an order',
             responses={200: 'Success', 404: 'Payment not found'})
    @api.marshal_with(payment_response_model)
    @jwt_required()
    def get(self, order_id):
        """Get payment status for an order"""
        payment = Payment.query.filter_by(order_id=order_id).first()
        if not payment:
            return {'status': 'pending'}, 200
        return {
            'id': payment.id,
            'order_id': payment.order_id,
            'amount_paid': payment.amount_paid,
            'payment_method': payment.payment_method,
            'payment_date': payment.payment_date,
            'payment_id': payment.payment_id,
            'status': payment.status or 'pending'
        }

    @api.doc('process_payment',
             description='Process payment for an order',
             responses={
                 201: 'Payment processed successfully',
                 400: 'Invalid payment data',
                 404: 'Order not found',
                 500: 'Payment processing error'
             })
    @api.expect(payment_model)
    @api.marshal_with(payment_response_model, code=201)
    @jwt_required()
    def post(self, order_id):
        """Process payment for an order"""
        try:
            # Get the order
            order = Order.query.get(order_id)
            if not order:
                api.abort(404, f"Order {order_id} not found")
                
            # Check if payment already exists
            existing_payment = Payment.query.filter_by(order_id=order_id).first()
            if existing_payment and existing_payment.status == 'completed':
                api.abort(400, f"Payment for order {order_id} already completed")

            # Get payment data
            data = request.get_json()
            payment_schema = PaymentSchema()
            
            # Validate payment amount matches order amount
            if abs(float(data['amount']) - order.total_amount) > 0.01:  # Allow small float difference
                api.abort(400, "Payment amount does not match order amount")

            # Create payment record
            payment_data = {
                'order_id': order_id,
                'amount_paid': data['amount'],
                'payment_method': data['payment_method'],
                'payment_id': data['payment_details'].get('payment_id', ''),
                'status': 'pending'  # Start with pending status
            }
            
            payment = Payment(**payment_data)
            
            try:
                # Here you would typically integrate with a payment processor
                # For now, we'll simulate payment processing
                payment.status = 'completed'  # Only set to completed after successful processing
                order.payment_status = 'completed'  # Update order payment status
                
                # Save changes
                db.session.add(payment)
                db.session.commit()
                
                return payment_schema.dump(payment), 201
                
            except Exception as e:
                db.session.rollback()
                payment.status = 'failed'
                order.payment_status = 'failed'
                db.session.add(payment)
                db.session.commit()
                api.abort(500, f"Payment processing failed: {str(e)}")
                
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error processing payment: {str(e)}'}, 500
