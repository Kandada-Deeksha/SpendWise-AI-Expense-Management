from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.expense import Expense
from services.feature_service import generate_ml_features
from services.ml_service import predict_next_month_expense

from sqlalchemy import func, extract


budget_recommendation_bp = Blueprint(
    "budget_recommendation",
    __name__
)


@budget_recommendation_bp.route("/", methods=["GET"])
@jwt_required()
def recommend_budget():

    user_id = int(get_jwt_identity())

    # Get monthly spending history
    monthly_expenses = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            func.sum(Expense.amount).label("monthly_total")
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

    if not monthly_expenses:
        return jsonify({
            "error": "Not enough expense data to recommend a budget."
        }), 400

    total_monthly_spending = sum(
        float(row.monthly_total)
        for row in monthly_expenses
    )

    number_of_months = len(monthly_expenses)

    average_monthly_spending = (
        total_monthly_spending / number_of_months
    )

    # Default recommendation using historical spending
    safety_buffer = average_monthly_spending * 0.10

    historical_recommended_budget = (
        average_monthly_spending + safety_buffer
    )

    # Try ML-based prediction
    predicted_next_month_expense = None

    try:
        features = generate_ml_features(user_id)

        predicted_next_month_expense = (
            predict_next_month_expense(features)
        )

    except ValueError:
        # ML prediction is unavailable when
        # sufficient historical/profile data is missing.
        pass

    # If ML prediction is available, use it with
    # a 10% safety buffer.
    if predicted_next_month_expense is not None:

        ml_safety_buffer = (
            predicted_next_month_expense * 0.10
        )

        recommended_budget = (
            predicted_next_month_expense
            + ml_safety_buffer
        )

    else:

        ml_safety_buffer = None

        recommended_budget = (
            historical_recommended_budget
        )

    return jsonify({
        "average_monthly_spending": round(
            average_monthly_spending,
            2
        ),

        "historical_recommended_budget": round(
            historical_recommended_budget,
            2
        ),

        "predicted_next_month_expense": (
            round(
                predicted_next_month_expense,
                2
            )
            if predicted_next_month_expense is not None
            else None
        ),

        "ml_safety_buffer": (
            round(
                ml_safety_buffer,
                2
            )
            if ml_safety_buffer is not None
            else None
        ),

        "recommended_monthly_budget": round(
            recommended_budget,
            2
        ),

        "months_analyzed": number_of_months,

        "currency": "INR"
    }), 200