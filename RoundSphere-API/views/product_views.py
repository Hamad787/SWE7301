from flask_restx import Resource, fields
from flask import request
from app import api
from models.product import Product
from schemas.product_schema import ProductSchema
from extensions import db
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

# Define request and response models for Swagger documentation
product_model = api.model('Product', {
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=True, description='Product description'),
    'price': fields.Float(required=True, description='Product price'),
    'stock': fields.Integer(required=True, description='Product stock quantity')
})

product_response_model = api.model('ProductResponse', {
    'id': fields.Integer(dump_only=True, description='Product ID'),
    'name': fields.String(description='Product name'),
    'description': fields.String(description='Product description'),
    'price': fields.Float(description='Product price'),
    'stock': fields.Integer(description='Product stock quantity')
})

class ProductViewSet(Resource):
    @jwt_required()
    @api.doc(description='Get all products or a single product by ID')
    @api.marshal_with(product_response_model, code=200)
    def get(self, product_id=None):
        """GET /api/products/ or /api/products/<product_id>"""
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return ProductSchema().dump(product), 200
            return {'message': 'Product not found'}, 404
        else:
            products = Product.query.all()
            return ProductSchema(many=True).dump(products), 200

    @jwt_required()
    @api.doc(description='Create a new product')
    @api.expect(product_model)
    @api.marshal_with(product_response_model, code=201)
    def post(self):
        """POST /api/products/"""
        data = request.get_json()
        product_schema = ProductSchema()
        try:
            product_data = product_schema.load(data)
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            return product_schema.dump(product), 201
        except ValidationError as err:
            return err.messages, 400

    @jwt_required()
    @api.doc(description='Update an existing product')
    @api.expect(product_model)
    @api.marshal_with(product_response_model, code=200)
    def put(self, product_id):
        """PUT /api/products/<product_id>"""
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        data = request.get_json()
        try:
            product_schema = ProductSchema()
            updated_product = product_schema.load(data, instance=product)
            db.session.commit()
            return product_schema.dump(updated_product)
        except ValidationError as err:
            return err.messages, 400

    @jwt_required()
    @api.doc(description='Delete an existing product')
    @api.marshal_with(product_response_model, code=200)
    def delete(self, product_id):
        """DELETE /api/products/<product_id>"""
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 200
