from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract

from models.expense import Expense
from models.budget import Budget


alert_bp = Blueprint(
    "alerts",
    __name__
)


@alert_bp.route("/", methods=["GET"])
@jwt_required()
def get_alerts():

    user_id = int(get_jwt_identity())

    # Get the current year and month from the latest expense
    latest_expense = (
        Expense.query
        .filter_by(user_id=user_id)
        .order_by(Expense.expense_date.desc())
        .first()
    )

    if not latest_expense:
        return jsonify({
            "alerts": [],
            "message": "No expense data available."
        }), 200

    current_year = latest_expense.expense_date.year
    current_month = latest_expense.expense_date.month

    # Calculate total spending for the latest month
    monthly_spending = (
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

    monthly_spending = float(monthly_spending or 0)

    # Find the budget for the same month
    budget = (
        Budget.query
        .filter_by(
            user_id=user_id,
            month=current_month,
            year=current_year
        )
        .first()
    )

    alerts = []

    if budget:

        budget_amount = float(budget.amount)

        if monthly_spending > budget_amount:

            alerts.append({
                "type": "budget_exceeded",
                "severity": "high",
                "message": (
                    f"You have exceeded your monthly budget by "
                    f"₹{monthly_spending - budget_amount:.2f}."
                )
            })

        else:

            usage_percentage = (
                monthly_spending / budget_amount
            ) * 100

            if usage_percentage >= 80:

                alerts.append({
                    "type": "budget_nearing_limit",
                    "severity": "medium",
                    "message": (
                        f"You have used {usage_percentage:.2f}% "
                        f"of your monthly budget."
                    )
                })

            else:

                alerts.append({
                    "type": "budget_healthy",
                    "severity": "low",
                    "message": (
                        f"You have used {usage_percentage:.2f}% "
                        f"of your monthly budget."
                    )
                })

    else:

        alerts.append({
            "type": "no_budget",
            "severity": "medium",
            "message": (
                "No budget has been set for the current month."
            )
        })

    return jsonify({
        "year": current_year,
        "month": current_month,
        "monthly_spending": round(
            monthly_spending,
            2
        ),
        "alerts": alerts,
        "currency": "INR"
    }), 200