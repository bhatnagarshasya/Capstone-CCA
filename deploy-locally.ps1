# Configuration
$DOCKERHUB_USERNAME = "bhatnagarshasya2002"
$IMAGE_NAME = "churn-analysis"
$SERVICE_NAME = "churn-analysis"

Write-Host "🚀 Starting deployment process..." -ForegroundColor Green

# Pull the latest image
Write-Host "📥 Pulling latest Docker image..." -ForegroundColor Cyan
docker pull "${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest"

# Apply Kubernetes configurations
Write-Host "📦 Applying Kubernetes configurations..." -ForegroundColor Cyan
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for deployment to be ready
Write-Host "⏳ Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl rollout status deployment/${IMAGE_NAME}

# Get the service URL
Write-Host "🔍 Getting service URL..." -ForegroundColor Cyan
Write-Host "🌐 Service is available at:" -ForegroundColor Green
minikube service ${SERVICE_NAME} --url

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "📊 To check the status of your deployment, run:" -ForegroundColor Cyan
Write-Host "   kubectl get pods" -ForegroundColor White
Write-Host "   kubectl get services" -ForegroundColor White 