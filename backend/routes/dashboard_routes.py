from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract

from models.expense import Expense
from models.budget import Budget
from models.savings_goal import SavingsGoal

from services.feature_service import generate_ml_features
from services.ml_service import predict_next_month_expense


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def dashboard_summary():

    user_id = int(get_jwt_identity())

    # Get the latest expense to determine the current month
    latest_expense = (
        Expense.query
        .filter_by(user_id=user_id)
        .order_by(Expense.expense_date.desc())
        .first()
    )

    if not latest_expense:
        return jsonify({
            "message": "No expense data available.",
            "total_expenses": 0,
            "monthly_expenses": 0,
            "category_wise_expenses": {},
            "budget": None,
            "savings_goals": [],
            "prediction": None,
            "currency": "INR"
        }), 200

    current_year = latest_expense.expense_date.year
    current_month = latest_expense.expense_date.month

    # Total expenses across all recorded transactions
    total_expenses = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            func.sum(Expense.amount)
        )
        .scalar()
    )

    total_expenses = float(total_expenses or 0)

    # Current month's total expenses
    monthly_expenses = (
        Expense.query
        .filter(
            Expense.user_id == user_id,
            extract("year", Expense.expense_date) == current_year,
            extract("month", Expense.expense_date) == current_month
        )
        .with_entities(
            func.sum(Expense.amount)
        )
        .scalar()
    )

    monthly_expenses = float(monthly_expenses or 0)

    # Category-wise spending for the current month
    category_results = (
        Expense.query
        .filter(
            Expense.user_id == user_id,
            extract("year", Expense.expense_date) == current_year,
            extract("month", Expense.expense_date) == current_month
        )
        .with_entities(
            Expense.category,
            func.sum(Expense.amount)
        )
        .group_by(Expense.category)
        .all()
    )

    category_wise_expenses = {
        row[0]: round(float(row[1]), 2)
        for row in category_results
    }

    # Current month's budget
    budget = (
        Budget.query
        .filter_by(
            user_id=user_id,
            month=current_month,
            year=current_year
        )
        .first()
    )

    budget_data = None

    if budget:

        budget_amount = float(budget.amount)

        remaining_budget = (
            budget_amount - monthly_expenses
        )

        usage_percentage = (
            (monthly_expenses / budget_amount) * 100
            if budget_amount > 0
            else 0
        )

        budget_data = {
            "amount": round(budget_amount, 2),
            "spent": round(monthly_expenses, 2),
            "remaining": round(remaining_budget, 2),
            "usage_percentage": round(
                usage_percentage,
                2
            )
        }

    # Savings goals
    savings_goals = (
        SavingsGoal.query
        .filter_by(user_id=user_id)
        .all()
    )

    savings_goal_data = [
        {
            "id": goal.id,
            "goal_name": goal.goal_name,
            "target_amount": round(
                float(goal.target_amount),
                2
            ),
            "target_date": goal.target_date.isoformat()
        }
        for goal in savings_goals
    ]

    # ML prediction
    prediction_data = None

    try:

        features = generate_ml_features(user_id)

        predicted_expense = (
            predict_next_month_expense(features)
        )

        recommended_budget = (
            predicted_expense * 1.10
        )

        prediction_data = {
            "predicted_next_month_expense": round(
                predicted_expense,
                2
            ),
            "recommended_next_month_budget": round(
                recommended_budget,
                2
            )
        }

    except ValueError:

        prediction_data = None

    except Exception:

        prediction_data = None

    return jsonify({
        "year": current_year,
        "month": current_month,
        "total_expenses": round(
            total_expenses,
            2
        ),
        "monthly_expenses": round(
            monthly_expenses,
            2
        ),
        "category_wise_expenses": category_wise_expenses,
        "budget": budget_data,
        "savings_goals": savings_goal_data,
        "prediction": prediction_data,
        "currency": "INR"
    }), 200