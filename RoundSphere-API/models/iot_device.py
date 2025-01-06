from extensions import db
class IoTDevice(db.Model):
    __tablename__ = 'iot_device'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50))

    def __repr__(self):
        return f"<IoTDevice {self.device_name}>"
