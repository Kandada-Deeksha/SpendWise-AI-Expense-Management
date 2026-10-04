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

    # If the user has no expenses yet, return an empty dashboard
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

    # ============================================================
    # TOTAL EXPENSES
    # ============================================================

    total_expenses = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            func.sum(Expense.amount)
        )
        .scalar()
    )

    total_expenses = float(total_expenses or 0)

    # ============================================================
    # CURRENT MONTH EXPENSES
    # ============================================================

    monthly_expenses = (
        Expense.query
        .filter(
            Expense.user_id == user_id,
            extract(
                "year",
                Expense.expense_date
            ) == current_year,
            extract(
                "month",
                Expense.expense_date
            ) == current_month
        )
        .with_entities(
            func.sum(Expense.amount)
        )
        .scalar()
    )

    monthly_expenses = float(monthly_expenses or 0)

    # ============================================================
    # CATEGORY-WISE CURRENT MONTH EXPENSES
    # ============================================================

    category_results = (
        Expense.query
        .filter(
            Expense.user_id == user_id,
            extract(
                "year",
                Expense.expense_date
            ) == current_year,
            extract(
                "month",
                Expense.expense_date
            ) == current_month
        )
        .with_entities(
            Expense.category,
            func.sum(Expense.amount)
        )
        .group_by(
            Expense.category
        )
        .all()
    )

    category_wise_expenses = {
        row[0]: round(float(row[1]), 2)
        for row in category_results
    }

    # ============================================================
    # CURRENT MONTH BUDGET
    # ============================================================

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

        budget_amount = float(
            budget.amount
        )

        remaining_budget = (
            budget_amount - monthly_expenses
        )

        usage_percentage = (
            (monthly_expenses / budget_amount) * 100
            if budget_amount > 0
            else 0
        )

        budget_data = {
            "amount": round(
                budget_amount,
                2
            ),
            "spent": round(
                monthly_expenses,
                2
            ),
            "remaining": round(
                remaining_budget,
                2
            ),
            "usage_percentage": round(
                usage_percentage,
                2
            )
        }

    # ============================================================
    # SAVINGS GOALS
    # ============================================================

    savings_goals = (
        SavingsGoal.query
        .filter_by(
            user_id=user_id
        )
        .order_by(
            SavingsGoal.target_date.asc()
        )
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
            "current_amount": round(
                float(goal.current_amount),
                2
            ),
            "target_date": (
                goal.target_date.isoformat()
                if goal.target_date
                else None
            )
        }
        for goal in savings_goals
    ]

    # ============================================================
    # ML PREDICTION
    # ============================================================

    prediction_data = None
    prediction_error = None

    try:

        features = generate_ml_features(
            user_id
        )

        predicted_expense = (
            predict_next_month_expense(
                features
            )
        )

        recommended_budget = (
            predicted_expense * 1.10
        )

        prediction_data = {
            "predicted_next_month_expense": round(
                float(predicted_expense),
                2
            ),
            "recommended_next_month_budget": round(
                float(recommended_budget),
                2
            )
        }

    except ValueError as exc:

        # Usually indicates that the user does not have
        # enough historical data or required ML features.
        prediction_error = str(exc)

    except Exception as exc:

        # Keep the API running, but preserve the actual
        # reason in the backend console instead of silently
        # hiding the problem.
        prediction_error = str(exc)

    if prediction_error:
        print(
            f"[Dashboard Prediction] "
            f"User {user_id}: {prediction_error}"
        )

    # ============================================================
    # FINAL DASHBOARD RESPONSE
    # ============================================================

    response_data = {
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
        "category_wise_expenses": (
            category_wise_expenses
        ),
        "budget": budget_data,
        "savings_goals": savings_goal_data,
        "prediction": prediction_data,
        "currency": "INR"
    }

    return jsonify(
        response_data
    ), 200
