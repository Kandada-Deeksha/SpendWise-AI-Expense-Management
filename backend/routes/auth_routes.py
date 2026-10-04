import re

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from extensions import db
from models.user import User


auth_bp = Blueprint("auth", __name__)


# =========================================================
# Validation Helpers
# =========================================================

USERNAME_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.]{2,19}$"
)

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_username(username):
    """
    Username rules:
    - 3 to 20 characters
    - Must start with a letter
    - Allows letters, numbers, underscore and dot
    - No spaces
    - No other special characters
    """
    if not isinstance(username, str):
        return False, "Username must be a valid text value."

    if not username:
        return False, "Username is required."

    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."

    if not USERNAME_PATTERN.fullmatch(username):
        return (
            False,
            "Username must start with a letter and contain only "
            "letters, numbers, underscores (_) or dots (.)."
        )

    return True, None


def validate_email(email):
    """
    Basic email format validation.
    """
    if not isinstance(email, str):
        return False, "Email must be a valid text value."

    email = email.strip()

    if not email:
        return False, "Email is required."

    if len(email) > 255:
        return False, "Email must not exceed 255 characters."

    if not EMAIL_PATTERN.fullmatch(email):
        return False, "Please enter a valid email address."

    return True, None


def validate_password(password):
    """
    Password rules:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - No spaces
    """
    if not isinstance(password, str):
        return False, "Password must be a valid text value."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if len(password) > 128:
        return False, "Password must not exceed 128 characters."

    if re.search(r"\s", password):
        return False, "Password must not contain spaces."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[^A-Za-z0-9\s]", password):
        return False, "Password must contain at least one special character."

    return True, None


# =========================================================
# User Registration
# =========================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    username = data.get("username")

    # Keep compatibility with the existing backend/database.
    # If an older frontend sends "name", it can still work.
    if not username:
        username = data.get("name")

    email = data.get("email")
    password = data.get("password")

    if not username:
        return jsonify({
            "error": "Username is required"
        }), 400

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    if not password:
        return jsonify({
            "error": "Password is required"
        }), 400

    # -----------------------------------------------------
    # Validate username
    # -----------------------------------------------------

    username_valid, username_error = validate_username(username)

    if not username_valid:
        return jsonify({
            "error": username_error
        }), 400

    # -----------------------------------------------------
    # Validate email
    # -----------------------------------------------------

    email = email.strip().lower()

    email_valid, email_error = validate_email(email)

    if not email_valid:
        return jsonify({
            "error": email_error
        }), 400

    # -----------------------------------------------------
    # Validate password
    # -----------------------------------------------------

    password_valid, password_error = validate_password(password)

    if not password_valid:
        return jsonify({
            "error": password_error
        }), 400

    # -----------------------------------------------------
    # Check whether email already exists
    # -----------------------------------------------------

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    # -----------------------------------------------------
    # Check whether username already exists
    #
    # Existing database uses the "name" column.
    # -----------------------------------------------------

    existing_username = User.query.filter_by(
        name=username
    ).first()

    if existing_username:
        return jsonify({
            "error": "Username already registered"
        }), 409

    # -----------------------------------------------------
    # Hash password
    # -----------------------------------------------------

    hashed_password = generate_password_hash(password)

    # -----------------------------------------------------
    # Create user
    # -----------------------------------------------------

    user = User(
        name=username,
        email=email,
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


# =========================================================
# User Login
# =========================================================

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

    email = data["email"].strip().lower()

    # -----------------------------------------------------
    # Find user by email
    # -----------------------------------------------------

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # -----------------------------------------------------
    # Check password
    # -----------------------------------------------------

    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # -----------------------------------------------------
    # Generate JWT
    # -----------------------------------------------------

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


# =========================================================
# Current User
# =========================================================

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