from flask import Blueprint, request, jsonify
from datetime import datetime

from extensions import db
from models.expense import Expense


expense_bp = Blueprint("expense", __name__)


# Test route
@expense_bp.route("/test", methods=["GET"])
def test_expense():
    return jsonify({
        "message": "Expense API is working!"
    })


# Add a new expense
@expense_bp.route("/", methods=["POST"])
def add_expense():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "user_id",
        "amount",
        "category",
        "expense_date"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    try:
        expense = Expense(
            user_id=data["user_id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description"),
            expense_date=datetime.strptime(
                data["expense_date"],
                "%Y-%m-%d"
            ).date()
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense added successfully",
            "expense_id": expense.id
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500


# Get all expenses for a user
@expense_bp.route("/", methods=["GET"])
def get_expenses():

    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({
            "error": "user_id is required"
        }), 400

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
            "amount": expense.amount,
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
def update_expense(expense_id):

    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({
            "error": "Expense not found"
        }), 404

    data = request.get_json()

    if "amount" in data:
        expense.amount = data["amount"]

    if "category" in data:
        expense.category = data["category"]

    if "description" in data:
        expense.description = data["description"]

    if "expense_date" in data:
        expense.expense_date = datetime.strptime(
            data["expense_date"],
            "%Y-%m-%d"
        ).date()

    try:
        db.session.commit()

        return jsonify({
            "message": "Expense updated successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500


# Delete an existing expense
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    expense = Expense.query.get(expense_id)

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

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500