from flask_restx import Resource, fields
from flask import request
from api import ns_data as api
from models.measurement_data import MeasurementData
from schemas.measurement_schema import MeasurementDataSchema
from extensions import db
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

# Define the measurement data request model for Swagger documentation
measurement_model = api.model('MeasurementData', {
    'device_id': fields.Integer(required=True, description='ID of the IoT Device'),
    'temperature': fields.Float(required=True, description='Temperature in Celsius'),
    'humidity': fields.Float(required=True, description='Humidity in percentage')
})

# Define the response model for Swagger documentation (for GET and POST responses)
measurement_response_model = api.model('MeasurementDataResponse', {
    'id': fields.Integer(dump_only=True, description='Measurement ID'),
    'device_id': fields.Integer(required=True, description='ID of the IoT Device'),
    'temperature': fields.Float(required=True, description='Temperature in Celsius'),
    'humidity': fields.Float(required=True, description='Humidity in percentage')
})

class MeasurementDataView(Resource):
    @jwt_required()
    @api.doc('get_measurement_data')  # Swagger route description
    @api.marshal_with(measurement_response_model, code=200)  # Return response format for successful GET
    def get(self):
        """GET /api/data"""
        """Fetch all measurement data"""
        measurements = MeasurementData.query.all()
        return MeasurementDataSchema(many=True).dump(measurements), 200

    @jwt_required()
    @api.doc('post_measurement_data')  # Swagger route description
    @api.expect(measurement_model)  # Expect input in the format of the measurement_model
    @api.marshal_with(measurement_response_model, code=201)  # Return response format for successful POST
    def post(self):
        """POST /api/data"""
        """Create new measurement data"""
        data = request.get_json()
        measurement_schema = MeasurementDataSchema()
        try:
            measurement_data = measurement_schema.load(data)
            measurement = MeasurementData(**measurement_data)
            db.session.add(measurement)
            db.session.commit()
            return measurement_schema.dump(measurement), 201
        except ValidationError as err:
            return err.messages, 400
