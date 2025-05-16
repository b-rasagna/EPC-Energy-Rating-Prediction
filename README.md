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

The pipeline is organized into two key phases: **Notebook Phase** and **Application Phase**, providing a comprehensive workflow from data exploration to deployment-ready inference.

---

### 1. Notebook Phase - Data Exploration, Model Training & Feature Engineering

This initial phase focuses on preparing and understanding the data, engineering meaningful features, and training predictive models:

* **Exploratory Data Analysis (EDA):**

  * Examine data distributions, missing values, and correlations within the EPC dataset.
  * Visualize energy ratings, cost metrics, and property attributes to inform feature selection.

* **Feature Engineering:**

  * Combine raw address components into full addresses for easy lookup.
  * Derive new features such as total energy cost, cost per area, and CO2 emissions per floor area.
  * Encode categorical variables and map energy ratings from letters (A-G) to numeric scores (6-0).

* **Model Training and Evaluation:**

  * Train multiple machine learning models (Random Forest, XGBoost, Logistic Regression, MLP) on the cleaned and processed dataset.
  * Evaluate models using metrics such as accuracy, macro F1 score, ROC-AUC, and log loss.
  * Compare models trained on imbalanced data and balanced data using SMOTE or class weighting.
  * Select the best-performing model(s) based on validation performance.

* **Model and Artifact Saving:**

  * Save trained models in `.pkl` format for ML models and `.h5` for any deep learning models.
  * Save preprocessing objects like label encoders, vectorizers, and tokenizers if applicable.
  * Generate a `lookup_df` CSV containing property keys (LMK\_KEY), full addresses, and selected features to enable efficient API-based querying.

---

### 2. Application Phase - Model Deployment & Real-Time Prediction

This phase covers how the trained models and artifacts are integrated into an API and UI for real-time predictions:

* **FastAPI Backend:**

  * Dynamically load the requested model into memory based on client requests.
  * Provide secure JWT-based authentication for all endpoints.
  * Implement API endpoints for user login, model selection, and prediction requests.
  * Support prediction requests by LMK\_KEY or property address, leveraging the precomputed `lookup_df` to fetch property features efficiently.
  * Return both numeric energy rating scores and human-readable letter ratings for user-friendly display.

* **Streamlit Frontend Dashboard:**

  * Offer a secure web UI where users log in using JWT-authenticated credentials.
  * Allow users to select a predictive model from the available list.
  * Enable input of either LMK\_KEY or full property address for energy rating prediction.
  * Display prediction results clearly, showing both the energy rating letter (A-G) and the underlying numeric score.
  * Provide error handling and informative messages for invalid inputs or missing data.

* **Lookup and Feature Retrieval:**

  * Use the generated `lookup_df` as a quick-access feature store mapping LMK\_KEY and addresses to their feature vectors.
  * Ensure the API performs fast, reliable lookups to support real-time predictions without retraining or reprocessing.

---

This modular and scalable pipeline ensures the system is **maintainable**, **extensible**, and **ready for production deployment**, enabling easy updates to models and datasets while delivering fast, accurate energy rating predictions to end-users.

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

* View prediction result (e.g., **B**)

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
  "predicted_potential_energy_rating": "B"
}
```

---

## Folder Structure

```
EPC_Energy_Rating_Predictor/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── model_selector.py
│   ├── prediction.py
│
├── models/
├── notebooks/                         
│   ├── Energy_Rating_Prediction.ipynb 
│   ├── Generate_Lookup_DF.ipynb
├── streamlit_app.py
├── run_app.sh
├── requirements.txt
├── Dockerfile 
├── .env 
├── notebook.ipynb
└── README.md
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
