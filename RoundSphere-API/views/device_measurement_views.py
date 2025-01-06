from flask_restx import Resource, fields
from flask import request
from api import ns_measurement as api
from models.device_measurement import DeviceMeasurement
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

# API models
location_model = api.model('Location', {
    'lat': fields.Float(required=True, description='Latitude'),
    'long': fields.Float(required=True, description='Longitude')
})

measurement_model = api.model('DeviceMeasurement', {
    'device_id': fields.String(required=True, description='IoT Device ID'),
    'temperature': fields.Float(required=True, description='Temperature reading'),
    'water_level': fields.Float(required=True, description='Water level reading'),
    'evaporation_rate': fields.Float(required=True, description='Evaporation rate'),
    'algae_concentration': fields.Float(required=True, description='Algae concentration'),
    'chlorine_level': fields.Float(required=True, description='Chlorine level'),
    'location': fields.Nested(location_model, required=True, description='Device location')
})

@api.route('/measurements')
class MeasurementListView(Resource):
    @api.doc('list_measurements',
             description='Get list of measurements with filtering options',
             params={
                 'device_id': 'Filter by device ID',
                 'start_date': 'Filter by start date (YYYY-MM-DD)',
                 'end_date': 'Filter by end date (YYYY-MM-DD)',
             })
    @jwt_required()
    def get(self):
        """Get list of measurements"""
        # Get query parameters
        device_id = request.args.get('device_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Build query
        query = DeviceMeasurement.query

        if device_id:
            query = query.filter_by(device_id=device_id)
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(DeviceMeasurement.timestamp >= start_date)
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(DeviceMeasurement.timestamp <= end_date)

        # Execute query
        measurements = query.order_by(DeviceMeasurement.timestamp.desc()).all()
        return [m.serialize for m in measurements]

    @api.doc('create_measurement')
    @api.expect(measurement_model)
    @jwt_required()
    def post(self):
        """Create a new measurement"""
        data = request.json

        try:
            measurement = DeviceMeasurement(
                device_id=data['device_id'],
                temperature=data['temperature'],
                water_level=data['water_level'],
                evaporation_rate=data['evaporation_rate'],
                algae_concentration=data['algae_concentration'],
                chlorine_level=data['chlorine_level'],
                location_lat=data['location']['lat'],
                location_long=data['location']['long']
            )
            
            db.session.add(measurement)
            db.session.commit()
            
            return {'message': 'Measurement recorded successfully', 'id': measurement.id}, 201
            
        except Exception as e:
            db.session.rollback()
            api.logger.error(f"Error creating measurement: {str(e)}")
            return {'error': str(e)}, 400

@api.route('/measurements/stats')
class MeasurementStatsView(Resource):
    @api.doc('get_measurement_stats',
             description='Get measurement statistics',
             params={
                 'device_id': 'Filter by device ID',
                 'days': 'Number of days to analyze (default: 7)'
             })
    @jwt_required()
    def get(self):
        """Get measurement statistics"""
        device_id = request.args.get('device_id')
        days = int(request.args.get('days', 7))
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query
        query = DeviceMeasurement.query.filter(
            DeviceMeasurement.timestamp >= start_date
        )
        
        if device_id:
            query = query.filter_by(device_id=device_id)
            
        measurements = query.all()
        
        if not measurements:
            return {'message': 'No data available for the specified period'}, 404
            
        # Calculate statistics
        stats = {
            'temperature': {
                'avg': sum(m.temperature for m in measurements) / len(measurements),
                'min': min(m.temperature for m in measurements),
                'max': max(m.temperature for m in measurements)
            },
            'water_level': {
                'avg': sum(m.water_level for m in measurements) / len(measurements),
                'min': min(m.water_level for m in measurements),
                'max': max(m.water_level for m in measurements)
            },
            'evaporation_rate': {
                'avg': sum(m.evaporation_rate for m in measurements) / len(measurements),
                'min': min(m.evaporation_rate for m in measurements),
                'max': max(m.evaporation_rate for m in measurements)
            }
        }
        
        return stats
