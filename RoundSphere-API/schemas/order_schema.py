from marshmallow import Schema, fields

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_name = fields.Str(required=True)
    customer_email = fields.Str(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)