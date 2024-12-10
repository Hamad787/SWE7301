from extensions import db
from sqlalchemy.orm import relationship

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    order_items = relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order #{self.id}>"
