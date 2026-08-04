# Troubleshooting Guide

Real issues encountered during this deployment, and how each was diagnosed and resolved.

## 1. Dockerfile installed the wrong database client

Symptom: Project required MySQL, but the supplied Dockerfile installed libpq-dev / libpq5 (PostgreSQL client libraries). Fix: replaced with default-libmysqlclient-dev and default-mysql-client.

## 2. .env file silently not created

Symptom: docker-compose up failed with env file not found, even after apparently creating the file in an editor. Cause: the file was opened in a new editor tab but never actually saved to disk. Fix: created the file directly from the terminal using a PowerShell here-string piped to Out-File.

## 3. JSON file rejected by AWS CLI despite looking correct

Symptom: aws ecs register-task-definition failed with Invalid JSON received, even though Get-Content displayed the file correctly. Cause: Out-File -Encoding utf8 in Windows PowerShell silently prepends a byte-order mark (BOM), which is invisible but breaks JSON parsing. Fix: used -Encoding ascii instead.

## 4. docker tag/push failing with a variable that looked set

Symptom: docker tag ems-app:latest $ECR_URI:latest failed with requires 2 arguments, even though echo $ECR_URI printed correctly. Cause: PowerShell interprets $VAR:text as a scope reference, breaking the substitution. Fix: wrapped the variable in braces, like dollarsign-brace-ECR_URI-brace:latest.

## 5. ECS task failing to pull the image from ECR

Symptom: Task stopped repeatedly with a dial tcp i/o timeout reaching ECR, when the ECS service ran in private subnets. Cause: Fargate tasks need outbound internet access to reach ECR and CloudWatch, and the private subnets had no route to the internet (no NAT Gateway, to avoid its cost). Fix: ran the ECS service in public subnets with a public IP instead, keeping the ECS security group locked down to only accept traffic from the ALB.

## 6. ECS task failing to create its CloudWatch log group

Symptom: AccessDeniedException for logs:CreateLogGroup. Cause: the AWS-managed execution role policy allows writing to existing log streams but not creating a brand new log group. Fix: created the log group manually ahead of time.

## 7. Database authentication failing despite matching-looking passwords

Symptom: Access denied for user admin when running migrate inside the live ECS task. Cause: the RDS master password had drifted from what was assumed to be in use - RDS never displays a master password back once set. Fix: explicitly reset the RDS master password and updated the task definition to match, then redeployed.

## 8. GitHub Actions CI/CD deploying to the wrong AWS account

Symptom: pipeline failed on the shared team repo with Could not find container definition with matching name, despite the container name being confirmed correct locally. Cause: the workflow used GitHub Secrets already configured on the team repo, pointing at a different shared AWS account with its own separate ECS setup. Fix: verified the pipeline worked correctly on a personal fork with dedicated credentials, and added a job-level repository check so the workflow skips cleanly rather than falsely failing when run in the shared repo context.

## 9. docker-compose.yml obsolete version warning

Symptom: every docker-compose command printed a warning about the version attribute being obsolete. Fix: removed the version key entirely.

## General lessons

PowerShell variables are session-scoped - closing a terminal or opening a new tab clears them, so always echo a variable to confirm it before using it in a command with real consequences. When multiple teammates share one AWS account and one CI/CD pipeline, do not add your own credentials to shared infrastructure without explicit authorization - validate in an isolated, self-owned account first.