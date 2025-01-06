from marshmallow import Schema, fields

class MeasurementDataSchema(Schema):
    id = fields.Int(dump_only=True)
    device_id = fields.Int(required=True)  
    timestamp = fields.DateTime(dump_only=True)  
    temperature = fields.Float()
    humidity = fields.Float()
    pressure = fields.Float()

