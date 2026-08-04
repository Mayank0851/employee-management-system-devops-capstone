# Deployment Guide

This guide documents how the Employee Management System was deployed to AWS, step by step, in the order it was actually built.

## Prerequisites

- AWS CLI configured with credentials (aws configure)
- Docker Desktop running locally
- Git, GitHub CLI access to your fork of the repo

## 1. Local application fixes

The supplied requirements.txt only listed django. It was updated to add the packages the Dockerfile and production setup require: django, gunicorn, mysqlclient, python-dotenv, whitenoise.

The supplied Dockerfile installed PostgreSQL client libraries (libpq-dev, libpq5) despite the project targeting MySQL. These were replaced with default-libmysqlclient-dev (builder stage) and default-mysql-client (production stage).

## 2. Docker and Docker Compose (local)

docker-compose.yml was completed with two services - app and database (MySQL 8.0) - connected on a shared bridge network, with credentials supplied via a gitignored .env file. Verified locally with docker-compose up --build and docker exec -it ems-app python manage.py migrate.

## 3. Amazon RDS (MySQL)

Engine: MySQL 8.0, instance class db.t3.micro (free-tier eligible). Not publicly accessible, placed in a private DB subnet group spanning two Availability Zones. DATABASES in settings.py already read connection details from environment variables - no code changes were required, only configuration.

## 4. VPC networking

One VPC (10.0.0.0/16). Two public subnets and two private subnets, across two Availability Zones. Internet Gateway attached, public route table pointing 0.0.0.0/0 at it. Three security groups, chained least-privilege: ALB SG allows 80/443 from anywhere, ECS SG allows 8000 only from the ALB SG, RDS SG allows 3306 only from the ECS SG.

## 5. Amazon ECR

aws ecr create-repository, docker build, docker tag, docker push - image pushed to the ECR repository.

## 6. ECS Fargate and Application Load Balancer

ECS cluster (ems-cluster), Fargate launch type. Task definition (256 CPU / 512 MB) referencing the ECR image, with an execution role for pulling images and writing logs. Target group (IP target type, required for Fargate), health check on /hello/. Internet-facing ALB across both public subnets, HTTP listener forwarding to the target group. ECS service running in the public subnets with a public IP assigned (not the originally planned private subnets - see Troubleshooting Guide for why).

## 7. GitHub Actions CI/CD

.github/workflows/ci.yml implements: checkout, configure AWS credentials, login to ECR, build/tag/push image, download current task definition, render new image ID, deploy to ECS, waiting for the service to stabilize. Authentication uses a dedicated IAM user (github-actions-ems) with GitHub Secrets, scoped to only the ECR and ECS actions the pipeline actually performs.

## 8. CloudWatch and SNS

Log group /ecs/ems-task receives container logs automatically. CloudWatch alarm ems-high-cpu watches ems-service CPU utilization, threshold 70% over a 5-minute period. SNS topic ems-alerts with an email subscription notifies on alarm state.

## 9. Security hardening

DB_USER / DB_PASSWORD moved out of the task definition plaintext environment block and into AWS Secrets Manager (ems/db-credentials), referenced via the task definition secrets array. IAM reviewed: ecsTaskExecutionRole uses only the AWS-managed execution policy plus a scoped inline policy for reading the one secret; github-actions-ems was tightened from AmazonECS_FullAccess down to a custom policy allowing only the specific ECS actions the pipeline needs.

## Verifying the deployment

curl http://<alb-dns-name>/hello/ should return 200 OK. Database connectivity was verified end-to-end by running python manage.py migrate inside the live ECS task via ECS Exec.