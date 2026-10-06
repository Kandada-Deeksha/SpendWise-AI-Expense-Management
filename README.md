SpendWise – AI-Powered Personal Expense Management & Prediction System

SpendWise is a web-based personal expense management and prediction system that helps users track expenses, analyze spending patterns, estimate next-month expenses, manage budgets, receive budget alerts, and track savings goals.

The project combines Machine Learning + Full Stack Development (FSD) to provide an end-to-end expense management application.

1. Key Features

User registration and login with JWT-based authentication

Personal financial profile management

Add, view, update, and delete expenses

Expense tracking dashboard

Monthly and category-wise expense analytics

Next-month expense prediction using a trained Machine Learning model

Personalized budget recommendation based on historical spending and predicted expenses

Budget creation and budget-vs-actual tracking

Budget usage alerts

Savings goal creation and progress tracking

React frontend

Flask backend REST API

Saved ML model and preprocessing artifacts

2. Machine Learning Pipeline

The ML pipeline follows these main stages:

Data collection

Data cleaning and preprocessing

Longitudinal/monthly dataset construction

Feature engineering

Chronological train-validation-test split

Training and comparison of multiple ML models

3-fold cross-validation during hyperparameter tuning

Hyperparameter optimization using GridSearchCV

Model evaluation using MAE, RMSE, and R²

Selection of the final Tuned Gradient Boosting model

Saving the trained model and preprocessing artifacts

Integration with the Flask backend for prediction

Models Compared

Linear Regression

Random Forest

Tuned Random Forest

Gradient Boosting

Tuned Gradient Boosting

Final Model

The final SpendWise prediction model is the Tuned Gradient Boosting model.

The target variable is the estimated next month's total expense.

The ML notebooks also use a chronological split so that future-month information is not used when training the model.

3. Repository Structure

SpendWise-AI-Expense-Management/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── ml_artifacts/
│   ├── final_spendwise_model.pkl
│   ├── encoder.pkl
│   ├── scaler.pkl
│   ├── selected_features.pkl
│   └── other saved ML artifacts
│
├── data_cleaning.ipynb
├── longitudinal_dataset_new.ipynb
├── feature_engineering.ipynb
├── raw_dataset.csv
├── spendwise_cleaned_dataset.csv
└── spendwise_longitudinal_dataset.csv

4. Technologies Used

Machine Learning

Python

Pandas

NumPy

Scikit-learn

Joblib

Jupyter Notebook

Backend

Flask

Flask-SQLAlchemy

Flask-JWT-Extended

Flask-CORS

PyMySQL

Python-dotenv

Frontend

React

Vite

Axios

React Router

Recharts

Lucide React

Database

MySQL

5. Running the Project Locally

Prerequisites

Install the following before running the project:

Python 3.x

Node.js and npm

MySQL Server

Git (optional)

6. Backend Setup

Open a terminal in the project root.

Step 1: Create and activate a Python virtual environment

Windows:

cd backend
python -m venv venv
venv\Scripts\activate

macOS/Linux:

cd backend
python3 -m venv venv
source venv/bin/activate

Step 2: Install Python dependencies

pip install -r requirements.txt

Step 3: Create the MySQL database

Open MySQL and create the project database:

CREATE DATABASE spendwise;

Step 4: Configure backend environment variables

Create a file named .env inside the backend folder.

Example:

DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=spendwise
JWT_SECRET_KEY=your_secret_key

Replace your_mysql_password with the password of your local MySQL user.

DB_HOST and DB_PORT can be left as localhost and 3306 for a standard local MySQL installation.

Step 5: Start the Flask backend

From the backend directory:

python app.py

The backend runs locally at:

http://127.0.0.1:5000

The root endpoint can be used to confirm that the backend is running:

http://127.0.0.1:5000/

Expected response:

{
  "message": "SpendWise Backend is running!"
}

7. Frontend Setup

Open a new terminal and move to the frontend directory:

cd frontend

Step 1: Install frontend dependencies

npm install

Step 2: Start the React development server

The backend CORS configuration allows the frontend origin http://localhost:5174, so start Vite on port 5174:

npm run dev -- --port 5174

The frontend will be available at:

http://localhost:5174

The frontend communicates with the Flask API through:

http://127.0.0.1:5000/api

8. Application Flow

The main application flow is:

User
  ↓
React Frontend
  ↓
Flask REST API
  ↓
MySQL Database
  ↓
ML Prediction Service
  ↓
Next-Month Expense Prediction
  ↓
Budget Recommendation / Alerts
  ↓
Prediction & Analytics shown in Frontend

For ML prediction specifically:

User/Financial Data
       ↓
Frontend Input
       ↓
Flask Prediction API
       ↓
Saved Encoder + Preprocessing Artifacts
       ↓
Saved SpendWise ML Model
       ↓
Predicted Next-Month Expense
       ↓
Frontend Output

9. Main Backend API Areas

The Flask backend provides API routes for:

Authentication

Expenses

Budgets

Savings Goals

Predictions

Budget Recommendations

Alerts

Dashboard

Analytics

Financial Profile

The application uses JWT authentication for protected user operations.

10. ML Artifacts

The trained ML artifacts are stored in the ml_artifacts directory.

Important files include:

final_spendwise_model.pkl – final trained prediction model

encoder.pkl – categorical feature encoder

scaler.pkl – saved preprocessing scaler

selected_features.pkl – selected model features

target_column.pkl – target variable information

Other saved training/test artifacts

These artifacts allow the trained model to be loaded by the Flask backend rather than retraining the model every time the application starts.

11. Model Evaluation

The ML pipeline evaluates the prediction models using:

Mean Absolute Error (MAE)

Root Mean Squared Error (RMSE)

R² Score

The project compares multiple models and uses 3-fold cross-validation during hyperparameter tuning.

The final model is then evaluated on a separate chronological test set.

12. Notebooks

The project contains the following main notebooks:

data_cleaning.ipynb

Used for cleaning and preparing the original dataset.

longitudinal_dataset_new.ipynb

Used to construct the longitudinal/monthly dataset required for historical expense analysis and prediction.

feature_engineering.ipynb

Contains feature engineering, model training, cross-validation, hyperparameter tuning, model comparison, and final evaluation.

13. Local Demo

For a local demonstration:

Start MySQL.

Start the Flask backend.

Start the React frontend on port 5174.

Open the frontend in a browser.

Register/login.

Complete the financial profile.

Add expenses.

Create a budget.

Open the dashboard.

View analytics, prediction, budget recommendation, alerts, and savings goals.

14. Deployment

This project is designed to run locally for the case-study demonstration.

A cloud-hosted deployment is not required for the current project setup.

For the academic demonstration, the application can be run using:

MySQL locally

Flask backend locally

React/Vite frontend locally

Saved ML artifacts locally

15. Project Objective

SpendWise aims to combine expense management with machine learning to help users:

Understand their spending patterns

Estimate future monthly expenses

Make informed budgeting decisions

Monitor budget usage

Receive timely alerts

Track progress toward savings goals

The overall approach is:

Track → Analyze → Predict → Recommend → Monitor

16. Notes

The ML model predicts the estimated next month's total expense; it is not an exact guarantee of future spending.

The current prediction pipeline is based on the features and categories represented in the trained ML dataset.

The application is intended as an academic ML + FSD case-study project.
