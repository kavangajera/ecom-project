from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.customer import Customer

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    customer = Customer.query.filter_by(email=data['email']).first()
    
    if customer and check_password_hash(customer.password, data['password']):
        login_user(customer)
        return jsonify({
            'message': 'Logged in successfully',
            'customer': {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'email': customer.email,
                'mobile': customer.mobile
            }
        })
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}) 