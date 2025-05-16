import os
import pickle

def load_model_by_name(model_name: str, model_objects: dict):
    """
    Loads a machine learning model based on the provided name.

    Parameters:
    - model_name (str): UI-displayed model name (mapped to filename)
    - model_objects (dict): In-memory store to update with the loaded model

    Raises:
    - ValueError: If an unknown model name is passed
    - FileNotFoundError: If the expected model file does not exist
    """

    # Reset model state before loading
    model_objects.update({
        "model": None,
        "feature_names": None,
        "type": None,
    })

    # Mapping from UI name to actual saved file
    model_file_map = {
        "Random Forest": "rf_model.pkl",
        "XGBoost": "xgb_model.pkl",
        "Logistic Regression": "log_model.pkl",
        "MLPClassifier": "mlp_model.pkl"
    }

    # Lookup model file
    model_file = model_file_map.get(model_name)
    if not model_file:
        raise ValueError(f"Unknown model name: '{model_name}'")

    file_path = os.path.join("models", model_file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Model file not found at path: {file_path}")

    # Load model using pickle
    with open(file_path, "rb") as f:
        model = pickle.load(f)

    model_objects["model"] = model
    model_objects["type"] = "ml"

    print(f"Model '{model_name}' loaded successfully.")