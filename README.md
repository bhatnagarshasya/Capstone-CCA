# Capstone-CCA
Capstone project: Predictive Customer Churn Analysis
Customer churn prediction software is a valuable tool for businesses seeking to retain their customer base. Leveraging machine learning algorithms and historical customer data, this software can identify patterns and early warning signs of potential churn. By analyzing factors such as customer behavior, satisfaction levels, and usage patterns, it empowers companies to take proactive measures, such as targeted marketing campaigns or personalized customer interactions, to reduce churn and increase customer loyalty. Ultimately, customer churn prediction software is a strategic asset that enhances customer retention efforts and contributes to long-term business success.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

1. **Testing**: Runs unit tests on every push and pull request
2. **Build**: Creates a Docker image
3. **Deploy**: Pushes the image to DockerHub

## Deployment

The application is containerized using Docker and can be deployed to Kubernetes.

### Prerequisites

- Docker
- Kubernetes cluster
- DockerHub account

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r MainApp/requirements.txt
   ```
3. Run the application:
   ```bash
   python MainApp/Routes.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t churn-analysis ./MainApp
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 churn-analysis
   ```

### Kubernetes Deployment

1. Update the image name in `k8s/deployment.yaml`
2. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/
   ```

## Monitoring

The application includes:
- Health check endpoint at `/health`
- Basic logging configuration
- Kubernetes liveness and readiness probes

## Future Improvements

- Infrastructure as Code (Terraform)
- Advanced monitoring with Prometheus and Grafana
- Automated database migrations
- Multi-environment deployment
- Security scanning
- Performance testing

Testing 123
