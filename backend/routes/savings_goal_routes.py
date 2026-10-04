from flask import Blueprint, request, jsonify
from datetime import datetime, date

from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.savings_goal import SavingsGoal


savings_goal_bp = Blueprint(
    "savings_goal",
    __name__
)


def validate_savings_goal_data(data, require_all=True):
    """Validate savings goal input data."""

    required_fields = [
        "goal_name",
        "target_amount",
        "target_date"
    ]

    if require_all:
        for field in required_fields:
            if field not in data:
                return f"{field} is required"

    # Validate goal name
    if "goal_name" in data:
        goal_name = data["goal_name"]

        if not isinstance(goal_name, str) or not goal_name.strip():
            return "goal_name must be a non-empty string"

        if len(goal_name.strip()) > 100:
            return "goal_name must not exceed 100 characters"

    # Validate target amount
    if "target_amount" in data:
        try:
            target_amount = float(data["target_amount"])
        except (TypeError, ValueError):
            return "target_amount must be a valid number"

        if target_amount <= 0:
            return "target_amount must be greater than 0"

    # Validate target date
    if "target_date" in data:
        try:
            target_date = datetime.strptime(
                data["target_date"],
                "%Y-%m-%d"
            ).date()
        except (TypeError, ValueError):
            return "target_date must be in YYYY-MM-DD format"

        if target_date <= date.today():
            return "target_date must be a future date"

    return None


# Create a savings goal
@savings_goal_bp.route("/", methods=["POST"])
@jwt_required()
def create_savings_goal():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    validation_error = validate_savings_goal_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        target_date = datetime.strptime(
            data["target_date"],
            "%Y-%m-%d"
        ).date()

        goal = SavingsGoal(
    user_id=user_id,
    goal_name=data["goal_name"].strip(),
    target_amount=float(data["target_amount"]),
    current_amount=float(data.get("current_amount", 0)),
    target_date=target_date
)

        db.session.add(goal)
        db.session.commit()

        return jsonify({
            "message": "Savings goal created successfully",
            "goal_id": goal.id
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to create savings goal"
        }), 500


# Get all savings goals for logged-in user
@savings_goal_bp.route("/", methods=["GET"])
@jwt_required()
def get_savings_goals():

    user_id = int(get_jwt_identity())

    goals = SavingsGoal.query.filter_by(
        user_id=user_id
    ).order_by(
        SavingsGoal.target_date.asc()
    ).all()

    result = []

    for goal in goals:
        result.append({
    "id": goal.id,
    "goal_name": goal.goal_name,
    "target_amount": float(goal.target_amount),
    "current_amount": float(goal.current_amount),
    "target_date": goal.target_date.isoformat(),
    "created_at": (
        goal.created_at.isoformat()
        if goal.created_at
        else None
    )
})

    return jsonify(result), 200


# Get a specific savings goal
@savings_goal_bp.route("/<int:goal_id>", methods=["GET"])
@jwt_required()
def get_savings_goal(goal_id):

    user_id = int(get_jwt_identity())

    goal = SavingsGoal.query.filter_by(
        id=goal_id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found"
        }), 404

    return jsonify({
    "id": goal.id,
    "goal_name": goal.goal_name,
    "target_amount": float(goal.target_amount),
    "current_amount": float(goal.current_amount),
    "target_date": goal.target_date.isoformat(),
    "created_at": (
        goal.created_at.isoformat()
        if goal.created_at
        else None
    )
}), 200


# Update a savings goal
@savings_goal_bp.route("/<int:goal_id>", methods=["PUT"])
@jwt_required()
def update_savings_goal(goal_id):

    user_id = int(get_jwt_identity())

    goal = SavingsGoal.query.filter_by(
        id=goal_id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    validation_error = validate_savings_goal_data(
        data,
        require_all=False
    )

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    if "goal_name" in data:
        goal.goal_name = data["goal_name"].strip()

    if "target_amount" in data:
        goal.target_amount = float(data["target_amount"])

    if "target_date" in data:
        goal.target_date = datetime.strptime(
            data["target_date"],
            "%Y-%m-%d"
        ).date()

    try:
        db.session.commit()

        return jsonify({
            "message": "Savings goal updated successfully"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to update savings goal"
        }), 500


# Delete a savings goal
@savings_goal_bp.route("/<int:goal_id>", methods=["DELETE"])
@jwt_required()
def delete_savings_goal(goal_id):

    user_id = int(get_jwt_identity())

    goal = SavingsGoal.query.filter_by(
        id=goal_id,
        user_id=user_id
    ).first()

    if not goal:
        return jsonify({
            "error": "Savings goal not found"
        }), 404

    try:
        db.session.delete(goal)
        db.session.commit()

        return jsonify({
            "message": "Savings goal deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to delete savings goal"
        }), 500