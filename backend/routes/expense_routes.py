from flask import Blueprint, request, jsonify
from datetime import datetime

from extensions import db
from models.expense import Expense

from flask_jwt_extended import jwt_required, get_jwt_identity


expense_bp = Blueprint("expense", __name__)


# Test route
@expense_bp.route("/test", methods=["GET"])
@jwt_required()
def test_expense():
    return jsonify({
        "message": "Expense API is working!"
    })


# Add a new expense
@expense_bp.route("/", methods=["POST"])
@jwt_required()
def add_expense():

    user_id = int(get_jwt_identity())

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "amount",
        "category",
        "expense_date"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # Validate amount
    try:
        amount = float(data["amount"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than 0"
        }), 400

    # Validate category
    category = data["category"]

    if not isinstance(category, str) or not category.strip():
        return jsonify({
            "error": "Category must be a non-empty string"
        }), 400

    # Validate date
    try:
        expense_date = datetime.strptime(
            data["expense_date"],
            "%Y-%m-%d"
        ).date()
    except (TypeError, ValueError):
        return jsonify({
            "error": "expense_date must be in YYYY-MM-DD format"
        }), 400

    try:
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category.strip(),
            description=data.get("description"),
            expense_date=expense_date
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense added successfully",
            "expense_id": expense.id
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to add expense"
        }), 500


# Get all expenses for logged-in user
@expense_bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():

    user_id = int(get_jwt_identity())

    expenses = Expense.query.filter_by(
        user_id=user_id
    ).order_by(
        Expense.expense_date.desc()
    ).all()

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "user_id": expense.user_id,
            "amount": float(expense.amount),
            "category": expense.category,
            "description": expense.description,
            "expense_date": expense.expense_date.isoformat(),
            "created_at": (
                expense.created_at.isoformat()
                if expense.created_at
                else None
            )
        })

    return jsonify(result), 200


# Update an existing expense
@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):

    user_id = int(get_jwt_identity())

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()

    if not expense:
        return jsonify({
            "error": "Expense not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Validate amount if provided
    if "amount" in data:

        try:
            amount = float(data["amount"])
        except (TypeError, ValueError):
            return jsonify({
                "error": "Amount must be a valid number"
            }), 400

        if amount <= 0:
            return jsonify({
                "error": "Amount must be greater than 0"
            }), 400

        expense.amount = amount

    # Validate category if provided
    if "category" in data:

        if (
            not isinstance(data["category"], str)
            or not data["category"].strip()
        ):
            return jsonify({
                "error": "Category must be a non-empty string"
            }), 400

        expense.category = data["category"].strip()

    if "description" in data:
        expense.description = data["description"]

    # Validate date if provided
    if "expense_date" in data:

        try:
            expense.expense_date = datetime.strptime(
                data["expense_date"],
                "%Y-%m-%d"
            ).date()
        except (TypeError, ValueError):
            return jsonify({
                "error": "expense_date must be in YYYY-MM-DD format"
            }), 400

    try:
        db.session.commit()

        return jsonify({
            "message": "Expense updated successfully"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to update expense"
        }), 500


# Delete an existing expense
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):

    user_id = int(get_jwt_identity())

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()

    if not expense:
        return jsonify({
            "error": "Expense not found"
        }), 404

    try:
        db.session.delete(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Failed to delete expense"
        }), 500