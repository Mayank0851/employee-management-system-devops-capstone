# 🚀 Employee Management System - DevOps Capstone Project

## 📖 Project Overview

This project demonstrates the deployment of a containerized Django-based Employee Management System on AWS using modern DevOps practices.

The application is containerized using Docker, stored in Amazon Elastic Container Registry (Amazon ECR), deployed on Amazon ECS using AWS Fargate, connected to Amazon RDS MySQL, exposed through an Application Load Balancer (ALB), secured with AWS Certificate Manager (ACM), and mapped to a custom domain using Amazon Route 53.

This project showcases end-to-end cloud deployment, container orchestration, networking, security, and AWS infrastructure management.

---

## 🌟 Features

- Dockerized Django application
- Multi-stage Docker build
- Gunicorn application server
- Amazon ECS deployment using AWS Fargate
- Amazon ECR integration
- Amazon RDS MySQL database
- Application Load Balancer
- HTTPS using AWS Certificate Manager (ACM)
- Custom domain using Amazon Route 53
- CloudWatch logging
- Environment variable based configuration
- GitHub Actions CI/CD

---

## 🏗️ Architecture

```
                    Internet
                        │
                        ▼
                 Amazon Route53
                        │
                        ▼
             AWS Certificate Manager
                  HTTPS Certificate
                        │
                        ▼
         Application Load Balancer (ALB)
                        │
                        ▼
             Amazon ECS Service
                        │
                        ▼
               AWS Fargate Task
                        │
                        ▼
      Docker Container (Gunicorn + Django)
                        │
                        ▼
               Amazon RDS MySQL
```

---

## ☁️ AWS Services Used

- Amazon ECS
- AWS Fargate
- Amazon ECR
- Amazon RDS
- Application Load Balancer
- Amazon Route53
- AWS Certificate Manager
- Amazon CloudWatch
- IAM
- VPC
- Security Groups

---

## 🛠️ Technology Stack

- Python 3.9
- Django 4.2.30
- Gunicorn 23.0.0
- Docker 29.6.2
- Docker Compose
- MySQL 8.0
- Git
- GitHub
- GitHub Actions

---

## 📁 Project Structure

```text
employee-management-system-devops-capstone/
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── employee_management_system/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
├── README.md
└── screenshots/
```

---

## 🔐 Environment Variables

The application uses environment variables for configuration.

Required variables:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DB_ENGINE
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

Refer to the `.env.example` file.

---

## 🚀 Deployment Workflow

1. Build Docker Image
2. Push Docker Image to Amazon ECR
3. Register ECS Task Definition
4. Deploy to Amazon ECS (AWS Fargate)
5. Connect to Amazon RDS
6. Configure Application Load Balancer
7. Configure HTTPS using ACM
8. Map Custom Domain using Route53

---

## 🚀 Local Setup

Clone the repository

```bash
git clone https://github.com/Mayank0851/employee-management-system-devops-capstone.git
```

Navigate into the project

```bash
cd employee-management-system-devops-capstone
```

Run Docker Compose

```bash
docker compose up --build
```

Access the application

```
http://localhost:8000/hello/
```

---

## 🌐 Live Demo

```
https://emsapp.nikhilgroup.click/hello/
```

---

## 🛠️ Challenges Faced

During the deployment, the following issues were encountered and resolved:

- IAM Role attachment for EC2 instance
- Amazon ECR authentication issues
- ECS task registration with Target Group
- ALB HTTP 503 errors
- Django ALLOWED_HOSTS configuration
- Route53 Alias configuration
- ACM SSL configuration
- ECS service redeployment after environment variable changes

---

## 🔄 CI/CD

GitHub Actions workflow automates:

- Repository Checkout
- Python Setup
- Dependency Installation
- Docker Build
- Amazon ECR Login
- Docker Image Push
- Amazon ECS Deployment

---

## 📸 Screenshots

Screenshots included:

- ECS Cluster
- ECS Service
- Amazon ECR
- Amazon RDS
- Application Load Balancer
- Route53
- ACM Certificate
- Live Application

---

## 🚀 Future Improvements

- AWS Secrets Manager
- ECS Auto Scaling
- CloudWatch Dashboard
- Terraform
- Blue/Green Deployment

---

## 👨‍💻 Author

**Nikhil Kumar Dubey**

GitHub: https://github.com/nikhildubeyofficial-blip

---

## 📄 License

This project is created for educational and portfolio purposes.
