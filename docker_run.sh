#!/bin/bash

# Variables
IMAGE_NAME="epc-energy-rating-app"
CONTAINER_NAME="epc-energy-rating-container"

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Stop and remove existing container if running
echo "Cleaning up old containers..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run the container
echo "Running Docker container..."
docker run --env-file .env \
           -p 8000:8000 \  # FastAPI
           -p 8501:8501 \  # Streamlit
           --name $CONTAINER_NAME \
           $IMAGE_NAME
