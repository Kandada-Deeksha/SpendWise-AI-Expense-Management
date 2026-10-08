from extensions import db
from datetime import datetime


class SavingsGoal(db.Model):
    __tablename__ = "savings_goals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    goal_name = db.Column(
        db.String(100),
        nullable=False
    )

    target_amount = db.Column(
        db.Float,
        nullable=False
    )

    current_amount = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    target_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )