# Docker Guide for Loan Default Prediction

This guide explains how to use Docker with the Loan Default Prediction project, including building, running, and managing the containerized application.

## Prerequisites

- Docker Desktop installed and running
- Basic familiarity with command line

## Project Overview

The loan default prediction project is containerized using Docker, making it easy to deploy and run consistently across different environments.

## Docker Image Details

- **Image Name:** `loan-default-prediction`
- **Base Image:** `python:3.11-slim`
- **Size:** ~2.5GB
- **Architecture:** ARM64 (Apple Silicon compatible)
- **Port:** 5000

## Building the Docker Image

### 1. Build the Image

```bash
# Build the Docker image
docker build -t loan-default-prediction .

# Build with specific tag
docker build -t loan-default-prediction:v1.0 .
```

### 2. Verify Build

```bash
# List all images
docker images

# Check specific image
docker images loan-default-prediction
```

## Running the Container

### 1. Basic Run

```bash
# Run the container (foreground)
docker run -p 5000:5000 loan-default-prediction

# Run in background (detached)
docker run -d -p 5000:5000 --name loan-app loan-default-prediction
```

### 2. Advanced Run Options

```bash
# Run with environment variables
docker run -d -p 5000:5000 \
  -e MLFLOW_TRACKING_URI="http://localhost:5001" \
  --name loan-app \
  loan-default-prediction

# Run with volume mounting (for data persistence)
docker run -d -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/mlruns:/app/mlruns \
  --name loan-app \
  loan-default-prediction

# Run with custom port mapping
docker run -d -p 8080:5000 --name loan-app loan-default-prediction
```

### 3. Interactive Mode

```bash
# Run with interactive shell
docker run -it --rm loan-default-prediction /bin/bash

# Run Python shell
docker run -it --rm loan-default-prediction python
```

## Container Management

### 1. View Running Containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### 2. Container Operations

```bash
# Start a stopped container
docker start loan-app

# Stop a running container
docker stop loan-app

# Restart a container
docker restart loan-app

# Remove a container
docker rm loan-app

# Remove a running container (force)
docker rm -f loan-app
```

### 3. Container Logs

```bash
# View container logs
docker logs loan-app

# Follow logs in real-time
docker logs -f loan-app

# View last 50 lines
docker logs --tail 50 loan-app
```

## Image Management

### 1. View Images

```bash
# List all images
docker images

# List images with specific name
docker images loan-default-prediction

# Show image details
docker inspect loan-default-prediction
```

### 2. Image Operations

```bash
# Remove an image
docker rmi loan-default-prediction

# Remove all unused images
docker image prune

# Remove all images (careful!)
docker rmi $(docker images -q)
```

## Docker Compose (Recommended)

Create a `docker-compose.yml` file for easier management:

```yaml
version: '3.8'

services:
  loan-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./mlruns:/app/mlruns
    environment:
      - MLFLOW_TRACKING_URI=http://localhost:5001
    container_name: loan-default-prediction

  mlflow:
    image: python:3.11-slim
    ports:
      - "5001:5000"
    command: >
      bash -c "pip install mlflow && 
               mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db"
    volumes:
      - ./mlruns:/mlruns
    container_name: mlflow-server
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

## Development Workflow

### 1. Development Mode

```bash
# Run with live code reloading
docker run -d -p 5000:5000 \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/templates:/app/templates \
  --name loan-dev \
  loan-default-prediction
```

### 2. Testing

```bash
# Run tests in container
docker run --rm loan-default-prediction python -m pytest

# Run specific test
docker run --rm loan-default-prediction python -m pytest tests/test_model.py
```

### 3. Debugging

```bash
# Run with debug mode
docker run -d -p 5000:5000 \
  -e FLASK_DEBUG=1 \
  --name loan-debug \
  loan-default-prediction

# Access container shell
docker exec -it loan-debug /bin/bash
```

## Production Deployment

### 1. Multi-stage Build (Optimized)

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### 2. Health Checks

```dockerfile
# Add to Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

### 3. Security Best Practices

```bash
# Run as non-root user
docker run -d -p 5000:5000 \
  --user 1000:1000 \
  --name loan-app \
  loan-default-prediction

# Limit resources
docker run -d -p 5000:5000 \
  --memory="1g" \
  --cpus="1.0" \
  --name loan-app \
  loan-default-prediction
```

## Troubleshooting

### 1. Common Issues

**Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Use different port
docker run -p 8080:5000 loan-default-prediction
```

**Container won't start:**
```bash
# Check logs
docker logs loan-app

# Run with debug
docker run -it --rm loan-default-prediction /bin/bash
```

**Permission issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Run with proper user
docker run --user $(id -u):$(id -g) loan-default-prediction
```

### 2. Debugging Commands

```bash
# Inspect container
docker inspect loan-app

# View container processes
docker exec loan-app ps aux

# Check container resources
docker stats loan-app

# View container filesystem
docker exec loan-app ls -la /app
```

### 3. Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

## Monitoring and Logs

### 1. Application Logs

```bash
# View application logs
docker logs -f loan-app

# Save logs to file
docker logs loan-app > app.log 2>&1
```

### 2. Resource Monitoring

```bash
# Monitor container resources
docker stats loan-app

# Monitor all containers
docker stats
```

## Best Practices

### 1. Image Optimization

- Use multi-stage builds
- Minimize layers
- Use .dockerignore file
- Remove unnecessary packages

### 2. Security

- Run as non-root user
- Use specific image tags
- Scan images for vulnerabilities
- Limit container resources

### 3. Development

- Use volumes for development
- Implement health checks
- Use environment variables
- Document container requirements

## Useful Commands Reference

```bash
# Build and run
docker build -t loan-default-prediction .
docker run -d -p 5000:5000 --name loan-app loan-default-prediction

# Management
docker ps -a
docker logs loan-app
docker stop loan-app
docker rm loan-app

# Cleanup
docker system prune -a
docker rmi loan-default-prediction

# Debugging
docker exec -it loan-app /bin/bash
docker inspect loan-app
docker stats loan-app
```

## Next Steps

1. **Deploy to Cloud:** Use AWS ECS, Google Cloud Run, or Azure Container Instances
2. **CI/CD Pipeline:** Set up automated builds with GitHub Actions
3. **Monitoring:** Implement logging and monitoring solutions
4. **Scaling:** Use Docker Swarm or Kubernetes for production scaling

---

**Last Updated:** January 2025  
**Docker Version:** 24.0.7  
**Project:** Loan Default Prediction
