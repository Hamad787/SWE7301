from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)  # Foreign Key for order
    product_id = fields.Int(required=True)  # Foreign Key for product
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)
    
