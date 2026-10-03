from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract

from models.expense import Expense


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_analytics():

    user_id = int(get_jwt_identity())

    monthly_results = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("total_expense")
        )
        .group_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date)
        )
        .order_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date)
        )
        .all()
    )

    monthly_data = [
        {
            "year": int(row.year),
            "month": int(row.month),
            "total_expense": round(float(row.total_expense), 2)
        }
        for row in monthly_results
    ]

    return jsonify({
        "monthly_expenses": monthly_data,
        "currency": "INR"
    }), 200


@analytics_bp.route("/categories", methods=["GET"])
@jwt_required()
def category_analytics():

    user_id = int(get_jwt_identity())

    category_results = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            Expense.category,
            func.sum(Expense.amount).label("total_expense")
        )
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    category_data = [
        {
            "category": row.category,
            "total_expense": round(float(row.total_expense), 2)
        }
        for row in category_results
    ]

    return jsonify({
        "category_expenses": category_data,
        "currency": "INR"
    }), 200