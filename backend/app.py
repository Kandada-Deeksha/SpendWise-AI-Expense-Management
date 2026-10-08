from flask import Flask
from flask_cors import CORS
from models.expense import Expense
from models.budget import Budget
from models.savings_goal import SavingsGoal
from routes.budget_routes import budget_bp
from routes.savings_goal_routes import savings_goal_bp
from routes.prediction_routes import prediction_bp
from routes.budget_recommendation_routes import budget_recommendation_bp
from routes.alert_routes import alert_bp
from routes.dashboard_routes import dashboard_bp
from routes.analytics_routes import analytics_bp
from models.financial_profile import FinancialProfile
from routes.financial_profile_routes import financial_profile_bp
from extensions import db
from config import Config
from routes.expense_routes import expense_bp
from models.user import User
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
JWTManager(app)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:5174",
            ]
        }
    },
    supports_credentials=True,
)

app.register_blueprint(
    expense_bp,
    url_prefix="/api/expenses"
)
app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)
app.register_blueprint(
    budget_bp,
    url_prefix="/api/budget"
)
app.register_blueprint(
    savings_goal_bp,
    url_prefix="/api/savings-goals"
)
app.register_blueprint(
    prediction_bp,
    url_prefix="/api/predictions"
)
app.register_blueprint(
    budget_recommendation_bp,
    url_prefix="/api/budget-recommendation"
)
app.register_blueprint(
    alert_bp,
    url_prefix="/api/alerts"
)
app.register_blueprint(
    dashboard_bp,
    url_prefix="/api/dashboard"
)
app.register_blueprint(
    analytics_bp,
    url_prefix="/api/analytics"
)
app.register_blueprint(
    financial_profile_bp,
    url_prefix="/api/financial-profile"
)
@app.route("/")
def home():
    return {
        "message": "SpendWise Backend is running!"
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=False)