from flask_restx import Resource, fields
from flask import request
from api import ns_products as api
from models.product import Product
from schemas.product_schema import ProductSchema
from extensions import db
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

# Define request and response models for Swagger documentation
product_model = api.model('Product', {
    'name': fields.String(required=True, description='Product name', example='Gaming Mouse'),
    'description': fields.String(required=True, description='Product description', example='High-precision gaming mouse with RGB lighting'),
    'price': fields.Float(required=True, description='Product price', example=59.99),
    'stock': fields.Integer(required=True, description='Product stock quantity', example=100)
})

product_response_model = api.inherit('ProductResponse', product_model, {
    'id': fields.Integer(description='Product ID', example=1),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api.route('/')
class ProductList(Resource):
    @api.doc('list_products',
             description='Get all products',
             responses={200: 'Success'})
    @api.marshal_list_with(product_response_model)
    @jwt_required()
    def get(self):
        """List all products"""
        products = Product.query.all()
        return ProductSchema(many=True).dump(products)

    @api.doc('create_product',
             description='Create a new product',
             responses={201: 'Product created', 400: 'Validation error'})
    @api.expect(product_model)
    @api.marshal_with(product_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new product"""
        try:
            product_schema = ProductSchema()
            product_data = product_schema.load(request.json)
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            return product_schema.dump(product), 201
        except ValidationError as err:
            api.abort(400, str(err.messages))

@api.route('/<int:product_id>')
@api.param('product_id', 'The product identifier')
class ProductDetail(Resource):
    @api.doc('get_product',
             description='Get a product by ID',
             responses={200: 'Success', 404: 'Product not found'})
    @api.marshal_with(product_response_model)
    @jwt_required()
    def get(self, product_id):
        """Get a product by ID"""
        product = Product.query.get_or_404(product_id)
        return ProductSchema().dump(product)

    @api.doc('update_product',
             description='Update a product',
             responses={200: 'Success', 404: 'Product not found', 400: 'Validation error'})
    @api.expect(product_model)
    @api.marshal_with(product_response_model)
    @jwt_required()
    def put(self, product_id):
        """Update a product"""
        product = Product.query.get_or_404(product_id)
        try:
            product_schema = ProductSchema()
            updated_product = product_schema.load(request.json, instance=product)
            db.session.commit()
            return product_schema.dump(updated_product)
        except ValidationError as err:
            api.abort(400, str(err.messages))

    @api.doc('delete_product',
             description='Delete a product',
             responses={200: 'Product deleted', 404: 'Product not found'})
    @jwt_required()
    def delete(self, product_id):
        """Delete a product"""
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}
