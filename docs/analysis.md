# Application Analysis

## Purpose

This document captures the pre-deployment analysis of the Employee Management
System Django application, completed before any infrastructure or deployment
work began, per Task 1 of the DevOps capstone.

## Technology Stack

- Language: Python 3.9
- Framework: Django
- WSGI server (production): Gunicorn
- Database driver: mysqlclient (MySQL/MariaDB)
- Static file serving: WhiteNoise

## Dependencies (as originally supplied)

The original requirements.txt contained only django - no production
server, database driver, or static file handler were included. This was
identified as incomplete during analysis and corrected as part of Task 2/3.

## Database

- As supplied: SQLite (django.db.backends.sqlite3), hardcoded file path
  under BASE_DIR.
- Configuration style: DATABASES dict already read ENGINE, NAME, USER,
  PASSWORD, HOST, and PORT from environment variables with SQLite as the
  fallback default - meaning the app was already structured to support an
  external database without code changes, only environment configuration.
- Production target: Amazon RDS for MySQL 8.0 (per Task 5 requirements).

## Application Entry Point

- Local/dev: python manage.py runserver
- Production (containerized): Gunicorn binds to 0.0.0.0:8000 and serves
  employee_management_system.wsgi:application
- Health check endpoint: /hello/ - used for container health checks and
  the ALB target group health check.

## Notable Findings During Analysis

- The Dockerfile shipped with the repo was mostly complete (multi-stage
  build, non-root user, health check) but installed PostgreSQL client
  libraries (libpq-dev, libpq5) despite the project requiring MySQL -
  corrected during Task 3.
- docker-compose.yml, .github/workflows/ci.yml, and the infrastructure/,
  config/, scripts/, and tests/ folders were intentionally left as
  placeholders/scaffolding for the DevOps team to complete.
- No .env or .env.example file was present; environment variable names
  expected by settings.py had to be inferred from the code itself.

## Conclusion

The application was functionally simple (a single Django view) but the
supporting deployment configuration was deliberately incomplete, consistent
with the project's stated goal of simulating a development-to-DevOps
handover. No changes were made to business logic (views.py, urls.py) at
any point in this project - all work was confined to deployment and
infrastructure configuration, per the project's stated constraints.