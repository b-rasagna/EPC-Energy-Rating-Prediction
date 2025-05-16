#!/bin/bash

# Config 
VENV_DIR=".venv"
FASTAPI_APP="app.main:app"
STREAMLIT_APP="streamlit_app.py"
MODEL_ARCHIVE="models/rf_model.pkl.tar.gz"
MODEL_DIR="models"

# Create virtual environment 
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Activate environment 
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install requirements 
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Extract model archive
echo "Extracting model archive $MODEL_ARCHIVE to $MODEL_DIR..."
tar -xzf $MODEL_ARCHIVE -C $MODEL_DIR

# Launch FastAPI 
echo "Starting FastAPI server (Uvicorn)..."
uvicorn $FASTAPI_APP --reload &

# Launch Streamlit 
echo "Starting Streamlit dashboard..."
streamlit run $STREAMLIT_APP