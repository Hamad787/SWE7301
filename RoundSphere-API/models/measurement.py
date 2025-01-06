from extensions import db
from datetime import datetime

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    height = db.Column(db.Float, nullable=False)
    chest = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float, nullable=False)
    inseam = db.Column(db.Float, nullable=False)
    shoulder = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    customer = db.relationship('User', backref=db.backref('measurements', lazy=True))

    def __repr__(self):
        return f'<Measurement {self.id} for Customer {self.customer_id}>'
