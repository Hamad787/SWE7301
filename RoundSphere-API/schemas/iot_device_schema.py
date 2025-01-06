from marshmallow import Schema, fields

class IoTDeviceSchema(Schema):
    id = fields.Int(dump_only=True)
    device_name = fields.Str(required=True)
    device_type = fields.Str(required=True)
    status = fields.Str()
