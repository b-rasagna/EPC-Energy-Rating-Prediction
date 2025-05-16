import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd

from app.auth import create_token, decode_token
from app.model_selector import load_model_by_name
from app.prediction import predict_epc_rating_by_lmk, predict_epc_rating_by_address

# Load environment variables from .env
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Initialize FastAPI App
app = FastAPI()

# In-memory store to hold the selected model and metadata
model_objects = {
    "model": None,
    "feature_names": None,
    "type": "ml"
}

# OAuth2 Configuration for JWT Token Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid or expired JWT token.")
    return user

# Simple user store (for demo purposes only)
users = {"admin": "pass123"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if users.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token(username)
    return {"access_token": token, "token_type": "bearer"}

# Request Models
class ModelRequest(BaseModel):
    model_name: str

class LMKPredictionRequest(BaseModel):
    lmk_key: str

class AddressPredictionRequest(BaseModel):
    address: str

# Load dataset for LMK_KEY lookup (preprocessed version with features)
lookup_df = pd.read_csv("models/epc_feature_lookup.csv", index_col="LMK_KEY")
lookup_df["ADDRESS_LOWER"] = lookup_df["PROPERTY_ADDRESS"].str.lower()

@app.post("/select_model")
def select_model(request: ModelRequest, user=Depends(verify_jwt_token)):
    try:
        load_model_by_name(request.model_name, model_objects)
        return {"message": f"Model '{request.model_name}' loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/by-lmk")
def predict_by_lmk(request: LMKPredictionRequest, user=Depends(verify_jwt_token)):
    return predict_epc_rating_by_lmk(request.lmk_key, model_objects, lookup_df)

@app.post("/predict/by-address")
def predict_by_address(request: AddressPredictionRequest, user=Depends(verify_jwt_token)):
    return predict_epc_rating_by_address(request.address, model_objects, lookup_df)