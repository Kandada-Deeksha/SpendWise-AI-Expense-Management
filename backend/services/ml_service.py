import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "..", "ml_artifacts")


MODEL_PATH = os.path.join(
    ARTIFACTS_DIR,
    "final_spendwise_model.pkl"
)

ENCODER_PATH = os.path.join(
    ARTIFACTS_DIR,
    "encoder.pkl"
)

SCALER_PATH = os.path.join(
    ARTIFACTS_DIR,
    "scaler.pkl"
)

SELECTED_FEATURES_PATH = os.path.join(
    ARTIFACTS_DIR,
    "selected_features.pkl"
)


model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
scaler = joblib.load(SCALER_PATH)
selected_features = joblib.load(SELECTED_FEATURES_PATH)


def predict_next_month_expense(data):
    """
    Predict next month's total expense using the trained SpendWise model.
    """

    input_data = pd.DataFrame([data])

    categorical_features = [
        "Occupation",
        "City_Tier"
    ]

    numerical_features = [
        feature
        for feature in selected_features
        if feature not in categorical_features
    ]

    # Encode categorical features
    encoded = encoder.transform(
        input_data[categorical_features]
    )

    encoded_columns = encoder.get_feature_names_out(
        categorical_features
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoded_columns,
        index=input_data.index
    )

    # Keep numerical features in the original training order
    numerical_df = input_data[numerical_features].copy()

    # Combine numerical + encoded categorical features
    processed_data = pd.concat(
        [
            numerical_df,
            encoded_df
        ],
        axis=1
    )

    # Ensure exact feature order used during training
    feature_order = list(
        scaler.feature_names_in_
    )

    processed_data = processed_data[
        feature_order
    ]

    # Scale features
    scaled_data = scaler.transform(
        processed_data
    )
    # Preserve feature names after scaling
    scaled_data = pd.DataFrame(
        scaled_data,
        columns=feature_order,
        index=processed_data.index
    )

    # Predict
    prediction = model.predict(
        scaled_data
    )[0]

    return float(prediction)