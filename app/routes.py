from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from . import create_app
from .models import User, Room, Message

app = create_app()
jwt = JWTManager(app)

@app.route('/api/users/register/', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Check if user already exists
    if User.get_by_username(data['username']):
        return jsonify({"message": "Username already exists."}), 400
    if User.get_by_email(data['email']):
        return jsonify({"message": "Email already registered."}), 400
    
    # Create new user
    try:
        User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            nickname=data.get('nickname')
        )
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        return jsonify({"message": "Registration failed.", "error": str(e)}), 500

@app.route('/api/users/token/', methods=['POST'])
def login_user():
    data = request.get_json()
    if User.verify_password(data['username'], data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid username or password"}), 401

@app.route('/api/users/profile/', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    user = User.get_by_username(current_user)
    if user:
        return jsonify({
            "username": user['username'],
            "email": user['email'],
            "nickname": user.get('nickname'),
            "created_at": user['created_at']
        }), 200
    return jsonify({"message": "User not found"}), 404