from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from extensions import db
from models.budget import Budget


budget_bp = Blueprint("budget", __name__)


def validate_budget_data(data, require_all=True):
    """Validate budget input data."""

    required_fields = ["amount", "month", "year"]

    if require_all:
        for field in required_fields:
            if field not in data:
                return f"{field} is required"

    if "amount" in data:
        try:
            amount = float(data["amount"])
        except (TypeError, ValueError):
            return "Amount must be a valid number"

        if amount <= 0:
            return "Amount must be greater than 0"

    if "month" in data:
        try:
            month = int(data["month"])
        except (TypeError, ValueError):
            return "Month must be a valid integer"

        if month < 1 or month > 12:
            return "Month must be between 1 and 12"

    if "year" in data:
        try:
            year = int(data["year"])
        except (TypeError, ValueError):
            return "Year must be a valid integer"

        if year < 2000 or year > 2100:
            return "Year must be between 2000 and 2100"

    return None


# Create a new budget
@budget_bp.route("/", methods=["POST"])
@jwt_required()
def create_budget():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    validation_error = validate_budget_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    try:
        budget = Budget(
            user_id=user_id,
            amount=float(data["amount"]),
            month=int(data["month"]),
            year=int(data["year"])
        )

        db.session.add(budget)
        db.session.commit()

        return jsonify({
            "message": "Budget created successfully",
            "budget_id": budget.id
        }), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "A budget already exists for this month and year."
        }), 409

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to create budget"
        }), 500


# Get all budgets for logged-in user
@budget_bp.route("/", methods=["GET"])
@jwt_required()
def get_budgets():

    user_id = int(get_jwt_identity())

    budgets = Budget.query.filter_by(
        user_id=user_id
    ).order_by(
        Budget.year.desc(),
        Budget.month.desc()
    ).all()

    result = []

    for budget in budgets:
        result.append({
            "id": budget.id,
            "amount": float(budget.amount),
            "month": budget.month,
            "year": budget.year,
            "created_at": (
                budget.created_at.isoformat()
                if budget.created_at
                else None
            )
        })

    return jsonify(result), 200


# Get a specific budget
@budget_bp.route("/<int:budget_id>", methods=["GET"])
@jwt_required()
def get_budget(budget_id):

    user_id = int(get_jwt_identity())

    budget = Budget.query.filter_by(
        id=budget_id,
        user_id=user_id
    ).first()

    if not budget:
        return jsonify({
            "error": "Budget not found"
        }), 404

    return jsonify({
        "id": budget.id,
        "amount": float(budget.amount),
        "month": budget.month,
        "year": budget.year,
        "created_at": (
            budget.created_at.isoformat()
            if budget.created_at
            else None
        )
    }), 200


# Update a budget
@budget_bp.route("/<int:budget_id>", methods=["PUT"])
@jwt_required()
def update_budget(budget_id):

    user_id = int(get_jwt_identity())

    budget = Budget.query.filter_by(
        id=budget_id,
        user_id=user_id
    ).first()

    if not budget:
        return jsonify({
            "error": "Budget not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    validation_error = validate_budget_data(
        data,
        require_all=False
    )

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    if "amount" in data:
        budget.amount = float(data["amount"])

    if "month" in data:
        budget.month = int(data["month"])

    if "year" in data:
        budget.year = int(data["year"])

    try:
        db.session.commit()

        return jsonify({
            "message": "Budget updated successfully"
        }), 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "A budget already exists for this month and year."
        }), 409

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to update budget"
        }), 500


# Delete a budget
@budget_bp.route("/<int:budget_id>", methods=["DELETE"])
@jwt_required()
def delete_budget(budget_id):

    user_id = int(get_jwt_identity())

    budget = Budget.query.filter_by(
        id=budget_id,
        user_id=user_id
    ).first()

    if not budget:
        return jsonify({
            "error": "Budget not found"
        }), 404

    try:
        db.session.delete(budget)
        db.session.commit()

        return jsonify({
            "message": "Budget deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to delete budget"
        }), 500