from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


# User Registration
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "email",
        "password"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # Check whether email already exists
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    # Hash password
    hashed_password = generate_password_hash(
        data["password"]
    )

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    try:
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user.id
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500
        # User Login
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "email" not in data or not data["email"]:
        return jsonify({
            "error": "email is required"
        }), 400

    if "password" not in data or not data["password"]:
        return jsonify({
            "error": "password is required"
        }), 400

    # Find user by email
    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # Check password
    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 200