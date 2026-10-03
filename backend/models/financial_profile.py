from extensions import db
from datetime import datetime


class FinancialProfile(db.Model):
    __tablename__ = "financial_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    occupation = db.Column(
        db.String(100),
        nullable=False
    )

    city_tier = db.Column(
        db.String(50),
        nullable=False
    )

    monthly_income = db.Column(
        db.Float,
        nullable=False
    )

    desired_savings_percentage = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )