# RushPlate - AWS CI/CD Pipeline Project

A food delivery API built with FastAPI, demonstrating a complete AWS CI/CD pipeline using CodePipeline, CodeBuild, ECR, and ECS Fargate.

## 🏗️ Architecture

![Architecture Diagram](architecture-diagram.png)

## 🚀 Technologies Used

### Application
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Nginx** - Reverse proxy
- **Docker** - Containerization

### AWS Services
- **Amazon ECR** - Container image registry
- **Amazon ECS Fargate** - Serverless container orchestration
- **AWS CodePipeline** - CI/CD orchestration
- **AWS CodeBuild** - Build and test automation
- **IAM** - Access management and security

### DevOps
- **GitHub** - Source control
- **Docker Multi-stage builds** - Optimized container images
- **pytest** - Automated testing

## 📋 Features

- **Automated CI/CD Pipeline**: Push to GitHub triggers automatic build and deployment
- **Containerized Application**: Docker-based deployment for consistency
- **Serverless Infrastructure**: ECS Fargate eliminates server management
- **Health Checks**: Built-in health monitoring endpoints
- **Rolling Deployments**: Zero-downtime updates

## 🔄 CI/CD Pipeline Flow

1. **Source Stage**: CodePipeline detects changes in GitHub repository
2. **Build Stage**: CodeBuild executes buildspec.yml
   - Installs dependencies
   - Runs pytest tests
   - Builds Docker image
   - Pushes image to ECR
   - Creates imagedefinitions.json
3. **Deploy Stage**: ECS updates service with new container image
   - Rolling deployment strategy
   - Health checks ensure stability

## 📁 Project Structure

```
rushplate/
├── app/
│   ├── models/          # Pydantic models
│   ├── routers/         # API endpoints
│   ├── static/          # Frontend files
│   └── main.py          # FastAPI application
├── tests/               # pytest test suite
├── Dockerfile           # Multi-stage Docker build
├── buildspec.yml        # CodeBuild configuration
├── nginx.conf           # Nginx configuration
├── requirements.txt     # Python dependencies
└── start.sh            # Container startup script
```

## 🛠️ Setup Instructions

### Prerequisites
- AWS Account
- GitHub Account
- AWS CLI configured
- Docker installed (for local testing)

### Local Development

```bash
# Clone the repository
git clone https://github.com/Rishabh1623/rushplate-cicd-pipeline.git
cd rushplate-cicd-pipeline/rushplate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run locally
uvicorn app.main:app --reload
```

### AWS Deployment

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name rush-plate --region us-east-1
```

2. **Create ECS Cluster**
```bash
aws ecs create-cluster --cluster-name Rush-Plate-Cluster --region us-east-1
```

3. **Create ECS Task Definition** (via AWS Console or CLI)
   - Family: `rush-plate-task`
   - Container: `rush-plate-container`
   - Image: `<account-id>.dkr.ecr.us-east-1.amazonaws.com/rush-plate:latest`

4. **Set up CodePipeline**
   - Source: GitHub repository
   - Build: CodeBuild project
   - Deploy: ECS service

## 🧪 API Endpoints

- `GET /health` - Health check endpoint
- `GET /restaurants` - List all restaurants
- `GET /restaurants/{id}` - Get restaurant details
- `POST /orders` - Place an order
- `GET /orders` - List all orders
- `GET /orders/{id}` - Get order details

## 🔐 Security Features

- IAM roles for service authentication
- Security groups for network isolation
- ECR image scanning enabled
- Container health checks
- Non-root user in Docker (optional)

## 📊 Monitoring

- ECS CloudWatch metrics
- Container health checks
- Application logs in CloudWatch

## 💡 Key Learnings

This project demonstrates:
- Building production-ready Docker containers
- Implementing automated CI/CD pipelines
- Deploying serverless containers on AWS
- Infrastructure security best practices
- Zero-downtime deployment strategies

## 🎯 Future Enhancements

- [ ] Add Application Load Balancer
- [ ] Implement RDS database
- [ ] Add Terraform for IaC
- [ ] Multi-environment setup (dev/staging/prod)
- [ ] CloudWatch dashboards and alarms
- [ ] Auto-scaling policies
- [ ] HTTPS with ACM certificate

## 📝 License

This project is for educational purposes.

## 👤 Author

**Rishabh**
- GitHub: [@Rishabh1623](https://github.com/Rishabh1623)

---

Built with ❤️ to learn AWS DevOps practices
