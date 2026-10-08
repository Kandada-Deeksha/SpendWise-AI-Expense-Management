from services.ml_service import predict_next_month_expense


test_data = {
    "Age": 30,
    "Occupation": "Salaried",
    "City_Tier": "Tier 1",
    "Desired_Savings_Percentage": 20,
    "Desired_Savings": 10000,
    "Month_Number": 10,
    "Income": 50000,
    "Food_Expense": 8000,
    "Travel_Expense": 5000,
    "Entertainment_Expense": 3000,
    "Total_Expense": 30000,
    "Remaining_Income": 20000,
    "Remaining_Income_Percentage": 40,
    "Food_Percentage": 16,
    "Travel_Percentage": 10,
    "Entertainment_Percentage": 6,
    "Previous_Month_Total_Expense": 28000,
    "Previous_Month_Food_Expense": 7500,
    "Previous_Month_Travel_Expense": 4500,
    "Previous_Month_Entertainment_Expense": 3000,
    "Expense_Lag_2": 27000,
    "Expense_Lag_3": 26000,
    "Rolling_3_Month_Avg_Expense": 27000,
    "Monthly_Expense_Change": 2000,
    "Previous_Month_Food_Percentage": 15,
    "Previous_Month_Travel_Percentage": 9,
    "Previous_Month_Entertainment_Percentage": 6,
    "Previous_Month_Remaining_Income": 22000,
    "Previous_Month_Remaining_Income_Percentage": 44,
    "Previous_Month_Income": 50000,
    "Monthly_Income_Change": 0
}


prediction = predict_next_month_expense(test_data)

print("PREDICTION SUCCESSFUL")
print("Predicted Next Month Expense:", prediction)