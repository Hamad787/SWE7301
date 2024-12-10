from marshmallow import Schema, fields

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)  # Foreign Key for the order
    amount_paid = fields.Float(required=True)
    payment_date = fields.DateTime(dump_only=True)  # Automatically set during serialization
    payment_method = fields.Str()

    # Optional: You can add custom validation here if necessary
