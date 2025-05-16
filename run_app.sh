#!/bin/bash

# Config 
VENV_DIR=".venv"
FASTAPI_APP="app.main:app"
STREAMLIT_APP="streamlit_app.py"

# Step 1: Create virtual environment 
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Step 2: Activate environment 
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 3: Install requirements 
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Launch FastAPI 
echo "Starting FastAPI server (Uvicorn)..."
uvicorn $FASTAPI_APP --reload &

# Step 5: Launch Streamlit 
echo "Starting Streamlit dashboard..."
streamlit run $STREAMLIT_APP
