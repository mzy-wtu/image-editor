from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models.user import User

user_bp = Blueprint('user_api', __name__)

@user_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data.get('email')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@user_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']) or not user.is_active:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    login_user(user, remember=True)
    return jsonify({'message': 'Login successful', 'user': {'username': user.username, 'is_admin': user.is_admin}}), 200

@user_bp.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@user_bp.route('/api/admin/users', methods=['GET'])
@login_required
def get_users():
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    user_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'is_active': user.is_active,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for user in users]
    
    return jsonify({'users': user_list}), 200

@user_bp.route('/api/admin/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200
@user_bp.route('/api/login', methods=['GET'])
def get_login_status():
    if current_user.is_authenticated:
        return jsonify({'user': {'username': current_user.username, 'is_admin': current_user.is_admin}}), 200
    return jsonify({}), 200
