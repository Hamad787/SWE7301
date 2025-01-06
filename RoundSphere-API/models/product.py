from extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"
