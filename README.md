# EPC Energy Rating Prediction

This project is an end-to-end machine learning pipeline designed to predict the **Potential Energy Rating** of properties based on structured Energy Performance Certificate (EPC) data. It provides:

* A FastAPI backend with JWT authentication
* A secure Streamlit dashboard for real-time predictions
* A complete training notebook covering EDA, preprocessing, and model evaluation
* Comparison of ML models trained on EPC data

---

## Table of Contents

* [Overview](#overview)
* [Model Performance](#model-performance)
* [End-to-End Pipeline](#end-to-end-pipeline)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [API Reference](#api-reference)
* [Folder Structure](#folder-structure)
* [Testing](#testing)
* [Docker Support](#docker-support)

---

## Overview

The system allows users to:

* Train and evaluate models using a Jupyter notebook
* Save trained models and reuse them via FastAPI
* Make authenticated predictions using LMK\_KEY or Property Address
* Optionally allow manual feature entry for new properties

---

## Model Performance

| Model               | Accuracy | F1 (Macro) |
| ------------------- | -------- | ---------- |
| Random Forest       | 0.7908   | 0.6803     |
| XGBoost             | 0.7718   | 0.6579     |
| MLPClassifier       | 0.7222   | 0.5795     |
| Logistic Regression | 0.4696   | 0.3023     |

> **Recommended model for deployment**: Random Forest

---

## End-to-End Pipeline

### 1. Notebook Phase

* Perform EDA and feature engineering on EPC data
* Generate `lookup_df` with key features
* Train and evaluate multiple models
* Save final models to `models/` directory

### 2. Application Phase

* FastAPI loads selected model on demand
* Streamlit provides secure UI for search and prediction
* Lookup works by `LMK_KEY` or `Property Address`
* Prediction output includes both rating letter and numeric score

---

## Getting Started

### Requirements

* Python 3.11+
* pip
* Docker (optional)
* Linux/macOS or WSL (Windows Subsystem for Linux)

### .env Setup

Create a `.env` file in the project root with:

```env
JWT_SECRET=your_super_secret_key
JWT_ALGORITHM=HS256
```

### Quick Start

```bash
chmod +x run_app.sh
./run_app.sh
```

This will:

* Build and start FastAPI on `http://localhost:8000`
* Start Streamlit on `http://localhost:8501`

---

## Usage

### Streamlit Dashboard

Visit `http://localhost:8501`

* Login credentials:

  ```
  Username: admin
  Password: pass123
  ```

* Choose a model

* Enter LMK\_KEY or Property Address

* View prediction result (e.g., **B (score: 6)**)

---

## API Reference

All endpoints require a valid JWT token.

### 1. Login

`POST /login`

**Form Data:**

```bash
username=admin&password=pass123
```

**Response:**

```json
{ "access_token": "<JWT>", "token_type": "bearer" }
```

### 2. Select Model

`POST /select_model`

**Headers:**

```
Authorization: Bearer <JWT>
```

**Body:**

```json
{ "model_name": "Random Forest" }
```

### 3. Predict by LMK\_KEY

`POST /predict/by-lmk`

**Body:**

```json
{ "lmk_key": "1795390458252020032613265028200560" }
```

### 4. Predict by Address

`POST /predict/by-address`

```json
{ "address": "36, Lea Hall Green, B20 2AW" }
```

**Response:**

```json
{
  "lmk_key": "...",
  "property_address": "...",
  "predicted_potential_energy_rating": 6,
  "predicted_rating_letter": "B"
}
```

---

## Folder Structure

```
EPC_Energy_Rating_Predictor/
│
├── app/                  # FastAPI source code
│   ├── main.py           # API routes
│   ├── auth.py           # JWT logic
│   ├── model_selector.py # Load models
│   ├── prediction.py     # Inference logic
│
├── models/               # Trained model files (.pkl)
├── streamlit_app.py      # Streamlit UI
├── run_app.sh            # Start script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build config
├── .env                  # JWT secret keys
├── notebook.ipynb        # EDA + model training
└── README.md             # This file
```

---

## Testing

```bash
pytest tests/
```

Covers:

* Login and auth flow
* Model loading
* LMK/address-based prediction

---

## Docker Support

### Build and Run

```bash
docker build -t epc-energy-rating-app .
docker run --env-file .env -p 8000:8000 -p 8501:8501 epc-energy-rating-app
```

Or use helper script:

```bash
chmod +x run_app.sh
./run_app.sh
```

### Output

* FastAPI: [http://localhost:8000](http://localhost:8000)
* Streamlit: [http://localhost:8501](http://localhost:8501)

---
