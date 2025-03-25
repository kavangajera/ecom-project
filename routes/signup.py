from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.customer import Customer
from extensions import db

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'email', 'mobile', 'password']):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Check if email already exists
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Check if mobile already exists
    if Customer.query.filter_by(mobile=data['mobile']).first():
        return jsonify({'error': 'Mobile number already registered'}), 400
    
    try:
        # Create new customer
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            mobile=data['mobile'],
            password=generate_password_hash(data['password'])
        )
        
        db.session.add(new_customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer registered successfully',
            'customer': {
                'customer_id': new_customer.customer_id,
                'name': new_customer.name,
                'email': new_customer.email,
                'mobile': new_customer.mobile
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 