from marshmallow import Schema, fields

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_name = fields.Str(required=True)
    customer_email = fields.Str(required=True)
    total_amount = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
