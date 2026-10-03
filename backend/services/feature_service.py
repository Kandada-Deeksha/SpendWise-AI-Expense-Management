from datetime import date
from calendar import monthrange

from sqlalchemy import extract, func

from models.expense import Expense
from models.financial_profile import FinancialProfile


def get_monthly_expense_data(user_id):
    """
    Get monthly expense totals and category-wise expenses
    for a specific user.
    """

    rows = (
        Expense.query
        .filter_by(user_id=user_id)
        .with_entities(
            extract("year", Expense.expense_date).label("year"),
            extract("month", Expense.expense_date).label("month"),
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .group_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date),
            Expense.category
        )
        .order_by(
            extract("year", Expense.expense_date),
            extract("month", Expense.expense_date)
        )
        .all()
    )

    monthly_data = {}

    for row in rows:
        year = int(row.year)
        month = int(row.month)

        key = (year, month)

        if key not in monthly_data:
            monthly_data[key] = {
                "Food_Expense": 0.0,
                "Travel_Expense": 0.0,
                "Entertainment_Expense": 0.0
            }

        category = row.category.strip().lower()
        amount = float(row.total)

        if category == "food":
            monthly_data[key]["Food_Expense"] += amount

        elif category == "travel":
            monthly_data[key]["Travel_Expense"] += amount

        elif category == "entertainment":
            monthly_data[key]["Entertainment_Expense"] += amount

    for key, data in monthly_data.items():
        data["Total_Expense"] = (
            data["Food_Expense"]
            + data["Travel_Expense"]
            + data["Entertainment_Expense"]
        )

    return monthly_data


def previous_month(year, month, months_back=1):
    """
    Return the year and month for a previous month.
    """

    total_months = year * 12 + (month - 1)
    total_months -= months_back

    previous_year = total_months // 12
    previous_month_number = total_months % 12 + 1

    return previous_year, previous_month_number


def calculate_month_percentages(data, income):
    """
    Calculate spending percentages and remaining income.
    """

    total_expense = data["Total_Expense"]

    if income > 0:
        food_percentage = (
            data["Food_Expense"] / income
        ) * 100

        travel_percentage = (
            data["Travel_Expense"] / income
        ) * 100

        entertainment_percentage = (
            data["Entertainment_Expense"] / income
        ) * 100

        remaining_income = income - total_expense

        remaining_income_percentage = (
            remaining_income / income
        ) * 100

    else:
        food_percentage = 0
        travel_percentage = 0
        entertainment_percentage = 0
        remaining_income = 0
        remaining_income_percentage = 0

    return {
        "Food_Percentage": food_percentage,
        "Travel_Percentage": travel_percentage,
        "Entertainment_Percentage": entertainment_percentage,
        "Remaining_Income": remaining_income,
        "Remaining_Income_Percentage": remaining_income_percentage
    }


def generate_ml_features(user_id):
    """
    Generate the raw features required by the trained
    SpendWise ML model.
    """

    profile = (
        FinancialProfile.query
        .filter_by(user_id=user_id)
        .first()
    )

    if not profile:
        raise ValueError(
            "Financial profile not found. "
            "Please create your financial profile first."
        )

    monthly_data = get_monthly_expense_data(user_id)

    if not monthly_data:
        raise ValueError(
            "No expense history found."
        )

    if len(monthly_data) < 3:
        raise ValueError(
            "At least 3 months of expense history "
            "is required for ML prediction."
        )

    months = sorted(monthly_data.keys())

    current_year, current_month = months[-1]

    current = monthly_data[
        (current_year, current_month)
    ]

    previous_year, previous_month_number = previous_month(
        current_year,
        current_month,
        1
    )

    previous = monthly_data.get(
        (previous_year, previous_month_number),
        {
            "Food_Expense": 0.0,
            "Travel_Expense": 0.0,
            "Entertainment_Expense": 0.0,
            "Total_Expense": 0.0
        }
    )

    year_2, month_2 = previous_month(
        current_year,
        current_month,
        2
    )

    lag_2_data = monthly_data.get(
        (year_2, month_2),
        {"Total_Expense": 0.0}
    )

    year_3, month_3 = previous_month(
        current_year,
        current_month,
        3
    )

    lag_3_data = monthly_data.get(
        (year_3, month_3),
        {"Total_Expense": 0.0}
    )

    income = float(profile.monthly_income)

    desired_savings_percentage = float(
        profile.desired_savings_percentage
    )

    desired_savings = (
        income * desired_savings_percentage / 100
    )

    current_percentages = calculate_month_percentages(
        current,
        income
    )

    previous_percentages = calculate_month_percentages(
        previous,
        income
    )

    rolling_months = [
        monthly_data.get(
            previous_month(
                current_year,
                current_month,
                i
            ),
            {"Total_Expense": 0.0}
        )["Total_Expense"]
        for i in range(0, 3)
    ]

    rolling_3_month_avg = (
        sum(rolling_months) / 3
    )

    monthly_expense_change = (
        current["Total_Expense"]
        - previous["Total_Expense"]
    )

    monthly_income_change = 0.0

    features = {
        "Age": profile.age,
        "Occupation": profile.occupation,
        "City_Tier": profile.city_tier,
        "Desired_Savings_Percentage":
            desired_savings_percentage,
        "Desired_Savings":
            desired_savings,
        "Month_Number":
            current_month,
        "Income":
            income,

        "Food_Expense":
            current["Food_Expense"],
        "Travel_Expense":
            current["Travel_Expense"],
        "Entertainment_Expense":
            current["Entertainment_Expense"],
        "Total_Expense":
            current["Total_Expense"],

        "Remaining_Income":
            current_percentages["Remaining_Income"],
        "Remaining_Income_Percentage":
            current_percentages[
                "Remaining_Income_Percentage"
            ],

        "Food_Percentage":
            current_percentages["Food_Percentage"],
        "Travel_Percentage":
            current_percentages["Travel_Percentage"],
        "Entertainment_Percentage":
            current_percentages[
                "Entertainment_Percentage"
            ],

        "Previous_Month_Total_Expense":
            previous["Total_Expense"],
        "Previous_Month_Food_Expense":
            previous["Food_Expense"],
        "Previous_Month_Travel_Expense":
            previous["Travel_Expense"],
        "Previous_Month_Entertainment_Expense":
            previous["Entertainment_Expense"],

        "Expense_Lag_2":
            lag_2_data["Total_Expense"],
        "Expense_Lag_3":
            lag_3_data["Total_Expense"],

        "Rolling_3_Month_Avg_Expense":
            rolling_3_month_avg,

        "Monthly_Expense_Change":
            monthly_expense_change,

        "Previous_Month_Food_Percentage":
            previous_percentages["Food_Percentage"],
        "Previous_Month_Travel_Percentage":
            previous_percentages["Travel_Percentage"],
        "Previous_Month_Entertainment_Percentage":
            previous_percentages[
                "Entertainment_Percentage"
            ],

        "Previous_Month_Remaining_Income":
            previous_percentages["Remaining_Income"],

        "Previous_Month_Remaining_Income_Percentage":
            previous_percentages[
                "Remaining_Income_Percentage"
            ],

        "Previous_Month_Income":
            income,

        "Monthly_Income_Change":
            monthly_income_change
    }

    return features