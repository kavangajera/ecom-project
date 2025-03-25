from flask import Blueprint, jsonify
from flask_login import login_required
from models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
@login_required
def list_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        product_dict = {
            'product_id': product.product_id,
            'unit': product.unit,
            'rating': product.rating,
            'raters': product.raters,
            'description': product.description,
            'name': product.name,
            'category': product.category,
            'price': float(product.price) if product.price else None,
            'deleted_price': float(product.deleted_price) if product.deleted_price else None,
            'images': [{'image_id': img.image_id, 'image_url': img.image_url} for img in product.images]
        }
        products_list.append(product_dict)
    return jsonify(products_list)

@products_bp.route('/product/<int:product_id>', methods=['GET'])
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    product_dict = {
        'product_id': product.product_id,
        'unit': product.unit,
        'rating': product.rating,
        'raters': product.raters,
        'description': product.description,
        'name': product.name,
        'category': product.category,
        'price': float(product.price) if product.price else None,
        'deleted_price': float(product.deleted_price) if product.deleted_price else None,
        'images': [{'image_id': img.image_id, 'image_url': img.image_url} for img in product.images]
    }
    return jsonify(product_dict) 