from extensions import db
from datetime import datetime

class MeasurementData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('iot_device.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)

    def __repr__(self):
        return f"<MeasurementData for Device {self.device_id} at {self.timestamp}>"
