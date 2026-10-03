from flask import Flask
from flask_cors import CORS
from models.expense import Expense
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

CORS(app)

app.register_blueprint(
    expense_bp,
    url_prefix="/api/expenses"
)
app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)


@app.route("/")
def home():
    return {
        "message": "SpendWise Backend is running!"
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)