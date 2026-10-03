from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.financial_profile import FinancialProfile


financial_profile_bp = Blueprint(
    "financial_profile",
    __name__
)


def validate_profile_data(data):
    required_fields = [
        "age",
        "occupation",
        "city_tier",
        "monthly_income",
        "desired_savings_percentage"
    ]

    for field in required_fields:
        if field not in data:
            return f"{field} is required"

    try:
        age = int(data["age"])
    except (TypeError, ValueError):
        return "age must be a valid integer"

    if age < 18 or age > 100:
        return "age must be between 18 and 100"

    if not isinstance(data["occupation"], str) or not data["occupation"].strip():
        return "occupation must be a non-empty string"

    if not isinstance(data["city_tier"], str) or not data["city_tier"].strip():
        return "city_tier must be a non-empty string"

    try:
        monthly_income = float(data["monthly_income"])
    except (TypeError, ValueError):
        return "monthly_income must be a valid number"

    if monthly_income <= 0:
        return "monthly_income must be greater than 0"

    try:
        savings_percentage = float(
            data["desired_savings_percentage"]
        )
    except (TypeError, ValueError):
        return "desired_savings_percentage must be a valid number"

    if savings_percentage < 0 or savings_percentage > 100:
        return "desired_savings_percentage must be between 0 and 100"

    return None


# Create or update financial profile
@financial_profile_bp.route("/", methods=["POST"])
@jwt_required()
def create_or_update_profile():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    validation_error = validate_profile_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    profile = FinancialProfile.query.filter_by(
        user_id=user_id
    ).first()

    if profile:
        profile.age = int(data["age"])
        profile.occupation = data["occupation"].strip()
        profile.city_tier = data["city_tier"].strip()
        profile.monthly_income = float(data["monthly_income"])
        profile.desired_savings_percentage = float(
            data["desired_savings_percentage"]
        )

        message = "Financial profile updated successfully"

    else:
        profile = FinancialProfile(
            user_id=user_id,
            age=int(data["age"]),
            occupation=data["occupation"].strip(),
            city_tier=data["city_tier"].strip(),
            monthly_income=float(data["monthly_income"]),
            desired_savings_percentage=float(
                data["desired_savings_percentage"]
            )
        )

        db.session.add(profile)

        message = "Financial profile created successfully"

    try:
        db.session.commit()

        return jsonify({
            "message": message,
            "profile_id": profile.id
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to save financial profile"
        }), 500


# Get financial profile
@financial_profile_bp.route("/", methods=["GET"])
@jwt_required()
def get_financial_profile():

    user_id = int(get_jwt_identity())

    profile = FinancialProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return jsonify({
            "error": "Financial profile not found"
        }), 404

    return jsonify({
        "id": profile.id,
        "age": profile.age,
        "occupation": profile.occupation,
        "city_tier": profile.city_tier,
        "monthly_income": float(profile.monthly_income),
        "desired_savings_percentage": float(
            profile.desired_savings_percentage
        ),
        "created_at": (
            profile.created_at.isoformat()
            if profile.created_at
            else None
        )
    }), 200