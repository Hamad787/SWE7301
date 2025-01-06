from marshmallow import Schema, fields, post_load, EXCLUDE
from models.payment import Payment

class PaymentSchema(Schema):
    """Schema for Payment model"""
    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields
        
    id = fields.Integer(dump_only=True)
    order_id = fields.Integer(required=True)
    amount_paid = fields.Float(required=True, data_key='amount')  # Map amount to amount_paid
    payment_method = fields.String(required=True)
    payment_date = fields.DateTime(dump_only=True)

    @post_load
    def make_payment(self, data, **kwargs):
        """Create a Payment instance"""
        payment_data = {
            'order_id': data['order_id'],
            'amount_paid': data['amount_paid'],
            'payment_method': data['payment_method']
        }
        
        # Get payment details from request context
        request_data = self.context.get('request_data', {})
        if 'payment_details' in request_data:
            payment_data['payment_id'] = request_data['payment_details'].get('payment_id')
            payment_data['status'] = request_data['payment_details'].get('status', 'completed')
            
        return Payment(**payment_data)
