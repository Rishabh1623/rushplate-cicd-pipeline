# RushPlate - AWS CI/CD Pipeline Project

A production-ready food delivery API built with FastAPI, demonstrating enterprise-grade AWS CI/CD practices using CodePipeline, CodeBuild, ECR, and ECS Fargate.

## 🎯 Business Problem & Solution

### Problem Statement
Traditional food delivery platforms face challenges with:
- Manual deployment processes leading to human errors and downtime
- Inconsistent environments between development and production
- Slow time-to-market for new features
- High infrastructure maintenance costs
- Difficulty scaling during peak hours

### Solution Architecture
RushPlate solves these challenges through:
- **Automated CI/CD Pipeline**: Zero-touch deployments reduce errors and enable rapid feature releases
- **Containerization**: Consistent environments from development to production
- **Serverless Containers**: ECS Fargate eliminates server management overhead
- **Infrastructure Automation**: Repeatable, version-controlled deployments

## 🏗️ Architecture

![Architecture Diagram](architecture-diagram.png)

### Architecture Components
- **GitHub**: Source code repository with version control
- **AWS CodePipeline**: Orchestrates the entire CI/CD workflow
- **AWS CodeBuild**: Automated build, test, and Docker image creation
- **Amazon ECR**: Secure, scalable container image registry
- **Amazon ECS Fargate**: Serverless container orchestration
- **IAM**: Fine-grained access control and security

## 💰 Cost Analysis & Trade-offs

### Monthly Cost Breakdown (Estimated)
- **ECS Fargate** (0.25 vCPU, 0.5 GB): ~$10-15/month
- **ECR Storage** (few GB): ~$1-2/month
- **CodePipeline**: $1/month (first pipeline free)
- **CodeBuild**: ~$2-5/month (pay per build minute)
- **Data Transfer**: ~$1-3/month
- **Total**: ~$15-25/month for production workload

### Trade-offs & Design Decisions

#### ✅ Chosen: ECS Fargate
**Why:**
- No server management (reduces operational overhead)
- Pay only for container runtime (cost-efficient for variable traffic)
- Auto-scaling built-in
- Faster deployment than EC2-based solutions

**Trade-off:**
- Slightly higher cost per hour vs EC2 (~30% premium)
- Less control over underlying infrastructure
- Cold start latency for scaled-down services

**Business Justification:** Operational savings (no DevOps team managing servers) outweigh the 30% compute premium.

#### ✅ Chosen: CodePipeline + CodeBuild
**Why:**
- Native AWS integration (no credential management)
- Fully managed (no Jenkins servers to maintain)
- Pay-per-use pricing model
- Built-in security and compliance

**Trade-off:**
- Less flexible than Jenkins for complex workflows
- Vendor lock-in to AWS ecosystem
- Limited plugin ecosystem

**Business Justification:** $50-200/month saved on Jenkins EC2 costs, plus reduced maintenance burden.

#### ✅ Chosen: In-Memory Data Storage
**Why:**
- Simplifies demo and learning
- Zero database costs
- Faster development iteration

**Trade-off:**
- Data lost on container restart
- Not production-ready for real applications
- No data persistence or backup

**Production Path:** Migrate to RDS PostgreSQL (~$15-30/month) for persistence.

#### ✅ Chosen: Single-AZ Deployment
**Why:**
- Reduces costs for demo/learning project
- Simpler architecture
- Faster deployments

**Trade-off:**
- No high availability
- Single point of failure
- Not suitable for production

**Production Path:** Multi-AZ deployment adds ~50% cost but provides 99.99% availability.

## 🚀 Technologies Used

### Application Stack
- **FastAPI** - Modern, high-performance Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- **Nginx** - Reverse proxy for production-grade request handling
- **Pydantic** - Data validation and settings management
- **pytest** - Automated testing framework

### AWS Services
- **Amazon ECR** - Container image registry with vulnerability scanning
- **Amazon ECS Fargate** - Serverless container orchestration
- **AWS CodePipeline** - CI/CD orchestration and workflow automation
- **AWS CodeBuild** - Managed build service with Docker support
- **IAM** - Identity and access management

### DevOps Practices
- **Docker Multi-stage Builds** - Optimized container images (30-40% size reduction)
- **Infrastructure as Code** - Version-controlled buildspec.yml
- **Automated Testing** - pytest integration in CI pipeline
- **Rolling Deployments** - Zero-downtime updates
- **Health Checks** - Automated service monitoring

## 📋 Features

### Application Features
- RESTful API for restaurant browsing and ordering
- Real-time order status tracking
- Multi-restaurant support with menu management
- Responsive web interface

### DevOps Features
- **Automated CI/CD**: Push to GitHub triggers automatic deployment
- **Containerized Deployment**: Consistent environments across all stages
- **Automated Testing**: pytest runs on every commit
- **Image Versioning**: Git commit SHA-based Docker tags
- **Health Monitoring**: Built-in health check endpoints
- **Rolling Updates**: Zero-downtime deployments with automatic rollback

## 🔄 CI/CD Pipeline Flow

```
Developer Push → GitHub
       ↓
CodePipeline Triggered (Source Stage)
       ↓
CodeBuild Execution (Build Stage)
  ├─ Install Python dependencies
  ├─ Run pytest test suite
  ├─ Build Docker image (multi-stage)
  ├─ Tag with commit SHA
  ├─ Push to Amazon ECR
  └─ Generate imagedefinitions.json
       ↓
ECS Deployment (Deploy Stage)
  ├─ Pull new image from ECR
  ├─ Update task definition
  ├─ Rolling deployment (one task at a time)
  ├─ Health check validation
  └─ Complete deployment
```

**Average Pipeline Duration:** 3-5 minutes from commit to production

## 📁 Project Structure

```
rushplate-cicd-pipeline/
├── rushplate/
│   ├── app/
│   │   ├── models/          # Pydantic data models
│   │   │   ├── order.py     # Order and OrderItem models
│   │   │   └── restaurant.py # Restaurant and MenuItem models
│   │   ├── routers/         # API route handlers
│   │   │   ├── health.py    # Health check endpoint
│   │   │   ├── orders.py    # Order management API
│   │   │   └── restaurants.py # Restaurant browsing API
│   │   ├── static/          # Frontend assets
│   │   │   └── index.html   # Single-page application
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/               # pytest test suite
│   │   └── test_main.py     # API endpoint tests
│   ├── Dockerfile           # Multi-stage Docker build
│   ├── buildspec.yml        # CodeBuild configuration
│   ├── nginx.conf           # Nginx reverse proxy config
│   ├── requirements.txt     # Python dependencies
│   └── start.sh            # Container startup script
├── buildspec.yml            # Root-level buildspec for CodeBuild
└── README.md               # Project documentation
```

## 🚀 Setup & Deployment Guide

### Prerequisites
- AWS Account with appropriate permissions
- GitHub Account
- Basic understanding of Docker and AWS services

### Step 1: Launch EC2 Instance for Build Server

```bash
# Launch EC2 instance (Amazon Linux 2023 or Ubuntu 22.04)
# Instance type: t3.medium (2 vCPU, 4GB RAM)
# Storage: 20-30 GB
# Security Group: Allow SSH (port 22) from your IP

# Connect via SSH
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

### Step 2: Install Docker

**For Amazon Linux 2023:**
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (no need for sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

**For Ubuntu:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

### Step 3: Install AWS CLI

```bash
# Download AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Install unzip if not available
sudo yum install unzip -y  # Amazon Linux
# OR
sudo apt install unzip -y  # Ubuntu

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### Step 4: Configure AWS CLI

```bash
# Configure AWS credentials
aws configure

# Enter the following when prompted:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

### Step 5: Install Git

```bash
# Amazon Linux
sudo yum install git -y

# Ubuntu
sudo apt install git -y

# Verify installation
git --version
```

### Step 6: Clone Repository

```bash
# Clone the project
git clone https://github.com/Rishabh1623/rushplate-cicd-pipeline.git
cd rushplate-cicd-pipeline/rushplate

# Verify files
ls -la
```

### Step 7: Create AWS Resources

#### 7.1 Create ECR Repository
```bash
# Create ECR repository for Docker images
aws ecr create-repository \
  --repository-name rush-plate \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true

# Note the repositoryUri from output
```

#### 7.2 Build and Push Initial Docker Image
```bash
# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-east-1
ECR_REPO=rush-plate

# Build Docker image
docker build -t rushplate:latest .

# Tag for ECR
docker tag rushplate:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Push image to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
```

#### 7.3 Create IAM Roles

**ECS Task Execution Role:**
```bash
# Create trust policy file
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ecs-tasks.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# Create role
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://trust-policy.json

# Attach managed policy
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

#### 7.4 Create ECS Cluster
```bash
# Create Fargate cluster
aws ecs create-cluster \
  --cluster-name Rush-Plate-Cluster \
  --capacity-providers FARGATE FARGATE_SPOT \
  --region us-east-1
```

#### 7.5 Create CloudWatch Log Group
```bash
# Create log group for container logs
aws logs create-log-group \
  --log-group-name /ecs/rushplate \
  --region us-east-1
```

#### 7.6 Register ECS Task Definition
```bash
# Create task definition JSON
cat > task-definition.json <<EOF
{
  "family": "rush-plate-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::$AWS_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "rush-plate-container",
    "image": "$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rush-plate:latest",
    "portMappings": [{
      "containerPort": 80,
      "protocol": "tcp"
    }],
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/rushplate",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
EOF

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json
```

#### 7.7 Create ECS Service
```bash
# Create service (replace subnet and security group IDs)
aws ecs create-service \
  --cluster Rush-Plate-Cluster \
  --service-name rush-plate-service \
  --task-definition rush-plate-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --region us-east-1
```

### Step 8: Set Up CI/CD Pipeline

#### 8.1 Create CodeBuild Project
```bash
# Create CodeBuild service role first (via IAM console or CLI)
# Then create CodeBuild project

aws codebuild create-project \
  --name rushplate-build \
  --source type=GITHUB,location=https://github.com/Rishabh1623/rushplate-cicd-pipeline.git \
  --artifacts type=CODEPIPELINE \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/standard:7.0,computeType=BUILD_GENERAL1_SMALL,privilegedMode=true \
  --service-role arn:aws:iam::$AWS_ACCOUNT_ID:role/codebuild-service-role \
  --region us-east-1
```

#### 8.2 Create CodePipeline
```bash
# Create pipeline via AWS Console:
# 1. Go to CodePipeline → Create pipeline
# 2. Pipeline name: rush-plate-pipeline
# 3. Source: GitHub (connect your repository)
# 4. Build: CodeBuild (select rushplate-build project)
# 5. Deploy: Amazon ECS (select cluster and service)
```

### Step 9: Test the Pipeline

```bash
# Make a small change to trigger pipeline
cd rushplate-cicd-pipeline
echo "# Test change" >> README.md
git add README.md
git commit -m "Test pipeline trigger"
git push origin main

# Watch pipeline execution in AWS Console
# Pipeline URL: https://console.aws.amazon.com/codesuite/codepipeline/pipelines
```

### Step 10: Access Your Application

```bash
# Get the public IP of your ECS task
aws ecs list-tasks --cluster Rush-Plate-Cluster --region us-east-1

# Describe task to get network details
aws ecs describe-tasks \
  --cluster Rush-Plate-Cluster \
  --tasks <TASK-ARN> \
  --region us-east-1

# Access application
curl http://<PUBLIC-IP>/health
# Or open in browser: http://<PUBLIC-IP>/
```

## 🧪 API Endpoints

### Health & Monitoring
- `GET /health` - Service health check (used by ECS)

### Restaurant Management
- `GET /restaurants` - List all available restaurants
- `GET /restaurants/{id}` - Get specific restaurant with menu

### Order Management
- `POST /orders` - Place a new order
- `GET /orders` - List all orders
- `GET /orders/{id}` - Get specific order details
- `PUT /orders/{id}/status` - Update order status

## 🔐 Security Implementation

### Network Security
- Security groups restrict traffic to necessary ports only
- ECS tasks run in isolated VPC subnets
- No direct internet access to container internals

### Access Control
- IAM roles with least-privilege principle
- Service-to-service authentication via IAM
- No hardcoded credentials in code or containers

### Container Security
- Multi-stage Docker builds minimize attack surface
- Regular base image updates
- ECR image scanning for vulnerabilities
- Non-root user execution (optional enhancement)

### Pipeline Security
- GitHub webhook authentication
- Encrypted artifacts in S3
- Audit logging via CloudTrail

## 📊 Performance & Scalability

### Current Configuration
- **Container Resources**: 0.25 vCPU, 0.5 GB RAM
- **Startup Time**: ~30-45 seconds
- **Request Handling**: ~100-200 req/sec per container
- **Deployment Time**: 3-5 minutes end-to-end

### Scalability Considerations
- Horizontal scaling via ECS service auto-scaling
- Stateless design enables easy replication
- Nginx caching for static assets
- Database connection pooling ready (when RDS added)

## 💡 Key Learnings & Best Practices

### What This Project Demonstrates
1. **Modern DevOps Practices**: Automated CI/CD with AWS native tools
2. **Container Orchestration**: Serverless container management with Fargate
3. **Infrastructure Automation**: Repeatable deployments via buildspec
4. **Security First**: IAM roles, security groups, and least privilege
5. **Cost Optimization**: Serverless architecture reduces operational costs
6. **Production Readiness**: Health checks, rolling deployments, monitoring

### Real-World Applications
- **Startups**: Rapid feature deployment without DevOps team
- **Enterprises**: Standardized deployment pipeline across teams
- **Microservices**: Template for containerized service deployment
- **Learning**: Hands-on AWS DevOps experience

## 🎓 Skills Demonstrated

- AWS Cloud Architecture (ECS, ECR, CodePipeline, CodeBuild, IAM)
- Docker containerization and optimization
- CI/CD pipeline design and implementation
- RESTful API development with FastAPI
- Infrastructure automation and configuration management
- Security best practices and access control
- Cost optimization and trade-off analysis
- System design and architectural decision-making

## 📝 License

This project is for educational and portfolio purposes.

## 👤 Author

**Rishabh**
- GitHub: [@Rishabh1623](https://github.com/Rishabh1623)
- Project: [rushplate-cicd-pipeline](https://github.com/Rishabh1623/rushplate-cicd-pipeline)

---

**Built to demonstrate AWS DevOps expertise and cloud-native application deployment**
