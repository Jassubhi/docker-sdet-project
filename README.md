# SDET Automation Framework | Docker, Kubernetes & CI/CD

A hands-on Software Development Engineer in Test (SDET) project demonstrating API automation, database integration testing, containerization, Kubernetes orchestration, parallel test execution, and CI/CD.

## Tech Stack

- **Language:** Python
- **Test Framework:** pytest, pytest-xdist
- **API:** FastAPI, REST
- **Database:** PostgreSQL, psycopg
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (kind, kubectl)
- **CI/CD:** GitHub Actions
- **Reporting:** pytest-html, JUnit XML

## Project Architecture

```text
GitHub Actions
      |
      v
Docker Compose
      |
      +---- FastAPI Service
      |          |
      |          v
      +---- PostgreSQL
      |
      v
pytest Integration Tests
      |
      +---- API Validation
      +---- Database Validation
      +---- Negative Test Cases
      +---- Parallel Execution (3 workers)
      |
      v
HTML + JUnit XML Reports
```

The FastAPI and PostgreSQL services can also run in a local Kubernetes cluster using the configurations in the `k8s/` directory.

## Key Features

- Automated REST API integration testing with pytest
- PostgreSQL database validation
- Positive and negative API test scenarios
- Dockerized application and test execution
- Multi-container orchestration using Docker Compose
- Parallel testing using pytest-xdist
- Automated CI execution with GitHub Actions
- HTML and JUnit XML test reporting
- Kubernetes Deployments and Services
- Kubernetes scaling, self-healing, and log inspection
- Environment-based test configuration

## Running Tests with Docker Compose

Start the application and database:

```bash
docker compose up -d --build db api
```

Run integration tests:

```bash
docker compose run --rm tests
```

Run tests in parallel:

```bash
docker compose run --rm tests pytest -v -n 3 tests/test_integration.py
```

## Kubernetes Deployment

Create a local Kubernetes cluster:

```bash
kind create cluster --name sdet-cluster
```

Build and load the application image:

```bash
docker build -t sdet-fastapi:v1 ./app
kind load docker-image sdet-fastapi:v1 --name sdet-cluster
```

Deploy PostgreSQL and FastAPI:

```bash
kubectl --context kind-sdet-cluster apply -f k8s/postgres.yaml
kubectl --context kind-sdet-cluster rollout status deployment/postgres

kubectl --context kind-sdet-cluster apply -f k8s/api-deployment.yaml
kubectl --context kind-sdet-cluster rollout status deployment/sdet-api
```

Check application health:

```bash
kubectl --context kind-sdet-cluster get pods
```

Access the API:

```bash
kubectl --context kind-sdet-cluster port-forward service/sdet-api 8082:8000
```

Swagger UI: http://localhost:8082/docs

## Kubernetes Operations

Scale FastAPI to three replicas:

```bash
kubectl --context kind-sdet-cluster scale deployment/sdet-api --replicas=3
```

Inspect application logs:

```bash
kubectl --context kind-sdet-cluster logs -l app=sdet-api --prefix=true --tail=20 --max-log-requests=5
```

Inspect Deployment status:

```bash
kubectl --context kind-sdet-cluster describe deployment sdet-api
```

## CI/CD Pipeline

GitHub Actions automatically:

1. Checks out the repository
2. Validates Docker Compose configuration
3. Starts FastAPI and PostgreSQL containers
4. Executes integration tests using three parallel pytest workers
5. Generates HTML and JUnit XML reports
6. Uploads test reports as workflow artifacts
7. Collects container logs on failure
8. Cleans up containers

## Test Coverage

- Create an item using the REST API
- Retrieve an item using its ID
- Verify persisted data directly in PostgreSQL
- Validate HTTP 404 for nonexistent items
- Validate HTTP 422 for invalid requests

## Learning Outcomes

This project demonstrates practical experience with containerized integration testing, API/database validation, parallel test execution, Kubernetes operations, and CI/CD automation.

**Note:** This is a local development and portfolio project. Database credentials are for local testing only, and the Kubernetes PostgreSQL Deployment uses ephemeral storage.
