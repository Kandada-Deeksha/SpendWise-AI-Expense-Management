import joblib
import warnings

from sklearn.exceptions import InconsistentVersionWarning

warnings.simplefilter("error", InconsistentVersionWarning)

model_path = "../ml_artifacts/final_spendwise_model.pkl"

try:
    model = joblib.load(model_path)

    print("MODEL LOADED SUCCESSFULLY")
    print("MODEL TYPE:", type(model))
    print("N_FEATURES:", getattr(model, "n_features_in_", "Not available"))
    print(
        "FEATURE_NAMES:",
        getattr(model, "feature_names_in_", "Not available")
    )

except InconsistentVersionWarning as e:
    print("ORIGINAL SKLEARN VERSION:")
    print(e.original_sklearn_version)

except Exception as e:
    print("LOAD ERROR:", type(e).__name__)
    print("ERROR MESSAGE:", str(e))