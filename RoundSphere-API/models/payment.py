from datetime import datetime
from extensions import db

class Payment(db.Model):
    """Payment model"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    payment_id = db.Column(db.String(100))  # Added for PayPal payment_id
    status = db.Column(db.String(50), default='pending')  # Added for payment status
    
    # Relationship
    order = db.relationship('Order', backref='payments')

    def __repr__(self):
        return f"<Payment {self.payment_id} for Order #{self.order_id}>"
