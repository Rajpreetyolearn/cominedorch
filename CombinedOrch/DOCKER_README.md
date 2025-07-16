# Docker Setup for Educational Tool Chatbot

This guide explains how to build, run, and deploy the Educational Tool Chatbot using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)
- Your API keys (OpenAI, Mem0)

## Quick Start

### 1. Environment Setup

Copy the example environment file and add your API keys:

```bash
cp env.example .env
```

Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
MEM0_API_KEY=your_actual_mem0_api_key_here
```

### 2. Build and Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at `http://localhost:8000`

### 3. Stop the Application

```bash
docker-compose down
```

## Manual Docker Commands

### Build the Image

```bash
docker build -t educational-chatbot .
```

### Run the Container

```bash
docker run -d \
  --name chatbot \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e MEM0_API_KEY=your_mem0_api_key \
  educational-chatbot
```

### View Logs

```bash
# With docker-compose
docker-compose logs -f chatbot

# With docker
docker logs -f chatbot
```

### Stop and Remove Container

```bash
docker stop chatbot
docker rm chatbot
```

## Production Deployment

### Environment Variables

For production, set these environment variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
MEM0_API_KEY=your_mem0_api_key

# Optional
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### Health Checks

The Docker image includes health checks that verify the application is running:

```bash
# Check container health
docker ps

# Manual health check
curl http://localhost:8000/health
```

### Scaling with Docker Compose

```bash
# Scale to multiple instances
docker-compose up --scale chatbot=3

# Use with load balancer (nginx example included in docker-compose.yml)
```

## Development with Docker

### Development Mode

For development, you can mount your source code:

```bash
docker run -d \
  --name chatbot-dev \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e MEM0_API_KEY=your_mem0_api_key \
  educational-chatbot \
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Debugging

```bash
# Access container shell
docker exec -it chatbot bash

# View application logs
docker logs chatbot

# Monitor resource usage
docker stats chatbot
```

## Docker Image Details

### Base Image
- **Python 3.11 Slim**: Optimized for size and security
- **Non-root user**: Runs as `appuser` for security
- **Multi-stage build**: Optimized for production

### Image Size
- Approximately 200-300MB (depending on dependencies)

### Ports
- **8000**: FastAPI application port

### Volumes
- `/app/logs`: Application logs
- `/app/templates`: HTML templates

## Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker logs chatbot
   
   # Verify environment variables
   docker exec chatbot env | grep API_KEY
   ```

2. **Health check failing**
   ```bash
   # Test health endpoint manually
   curl http://localhost:8000/health
   
   # Check if port is accessible
   docker port chatbot
   ```

3. **Permission issues**
   ```bash
   # The container runs as non-root user
   # Ensure mounted volumes have correct permissions
   chmod -R 755 ./logs
   ```

### Performance Optimization

1. **Memory limits**
   ```bash
   docker run --memory=512m educational-chatbot
   ```

2. **CPU limits**
   ```bash
   docker run --cpus=1.0 educational-chatbot
   ```

3. **Production settings**
   ```bash
   # Use multiple workers for production
   docker run -e WORKERS=4 educational-chatbot
   ```

## Security Considerations

- Container runs as non-root user
- No sensitive data in image layers
- Environment variables for secrets
- Regular security updates recommended

## Support

For issues related to Docker deployment, check:
1. Container logs: `docker logs chatbot`
2. Health endpoint: `http://localhost:8000/health`
3. Application metrics: `http://localhost:8000/analytics`

## Next Steps

- Set up CI/CD pipeline
- Configure monitoring and logging
- Add SSL/TLS termination
- Implement container orchestration (Kubernetes) 