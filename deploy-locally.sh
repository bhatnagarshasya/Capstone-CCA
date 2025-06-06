#!/bin/bash

# Exit on error
set -e

# Configuration
DOCKERHUB_USERNAME="bhatnagarshasya2002"  # Replace with your DockerHub username
IMAGE_NAME="churn-analysis"
SERVICE_NAME="churn-analysis"

echo "🚀 Starting deployment process..."

# Pull the latest image
echo "📥 Pulling latest Docker image..."
docker pull ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest

# Apply Kubernetes configurations
echo "📦 Applying Kubernetes configurations..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/${IMAGE_NAME}

# Get the service URL
echo "🔍 Getting service URL..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    minikube service ${SERVICE_NAME} --url
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    minikube service ${SERVICE_NAME} --url
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🌐 Service is available at:"
    minikube service ${SERVICE_NAME} --url
fi

echo "✅ Deployment completed successfully!"
echo "📊 To check the status of your deployment, run:"
echo "   kubectl get pods"
echo "   kubectl get services" 