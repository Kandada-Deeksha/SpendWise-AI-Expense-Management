from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.feature_service import generate_ml_features
from services.ml_service import predict_next_month_expense


prediction_bp = Blueprint(
    "prediction",
    __name__
)


@prediction_bp.route("/", methods=["POST"])
@jwt_required()
def predict_expense():

    user_id = int(get_jwt_identity())

    try:
        features = generate_ml_features(user_id)

        prediction = predict_next_month_expense(
            features
        )

        return jsonify({
            "user_id": user_id,
            "predicted_next_month_expense": round(
                prediction,
                2
            ),
            "currency": "INR"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except Exception:

        return jsonify({
            "error": "Failed to generate expense prediction"
        }), 500