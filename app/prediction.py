import numpy as np
import pandas as pd

# Reverse map: numeric rating to letter
rating_map_reverse = {6: 'G', 5: 'F', 4: 'E', 3: 'D', 2: 'C', 1: 'B', 0: 'A'}

def get_features_by_lmk(lmk_key: str, lookup_df: pd.DataFrame):
    if lmk_key in lookup_df.index:
        row = lookup_df.loc[lmk_key]
        return row.drop(['PROPERTY_ADDRESS', 'ADDRESS_LOWER']).values.reshape(1, -1), row['PROPERTY_ADDRESS']
    return None, None

def get_features_by_address(address: str, lookup_df: pd.DataFrame):
    match = lookup_df[lookup_df['ADDRESS_LOWER'] == address.lower()]
    if not match.empty:
        row = match.iloc[0]
        return row.drop(['PROPERTY_ADDRESS', 'ADDRESS_LOWER']).values.reshape(1, -1), row.name, row['PROPERTY_ADDRESS']
    return None, None, None

def predict_epc_rating_by_lmk(lmk_key: str, model_objects: dict, lookup_df: pd.DataFrame) -> dict:
    if not lmk_key or not isinstance(lmk_key, str):
        return {"error": "Invalid LMK_KEY. Please provide a valid property identifier."}

    if model_objects["model"] is None:
        return {"error": "No model loaded. Please select a model first."}

    if lmk_key not in lookup_df.index:
        return {"error": f"LMK_KEY '{lmk_key}' not found in dataset."}

    row = lookup_df.loc[lmk_key]
    features = row.drop(['PROPERTY_ADDRESS', 'ADDRESS_LOWER']).values.reshape(1, -1)

    try:
        prediction = model_objects["model"].predict(features)
        rating_numeric = int(prediction[0])
        rating_letter = rating_map_reverse.get(rating_numeric, "Unknown")
        return {
            "lmk_key": lmk_key,
            "property_address": row['PROPERTY_ADDRESS'],
            "predicted_potential_energy_rating": rating_numeric,
            "predicted_rating_letter": rating_letter
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

def predict_epc_rating_by_address(address: str, model_objects: dict, lookup_df: pd.DataFrame) -> dict:
    if not address or not isinstance(address, str):
        return {"error": "Invalid property address. Please provide a valid address."}

    if model_objects["model"] is None:
        return {"error": "No model loaded. Please select a model first."}

    features, lmk_key, full_address = get_features_by_address(address, lookup_df)
    if features is None:
        return {"error": f"Address '{address}' not found in dataset."}

    try:
        prediction = model_objects["model"].predict(features)
        rating_numeric = int(prediction[0])
        rating_letter = rating_map_reverse.get(rating_numeric, "Unknown")
        return {
            "lmk_key": lmk_key,
            "property_address": full_address,
            "predicted_potential_energy_rating": rating_numeric,
            "predicted_rating_letter": rating_letter
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}