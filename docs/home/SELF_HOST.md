# Self-Hosting Guide

This guide covers deploying Convergence in your own infrastructure.
Whether you're running a small personal instance or a large-scale deployment, we've got you covered.

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/prodigaltech/convergence.git
cd convergence

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services
docker-compose up -d
```

#### Using Docker Directly

```bash
# Build the image
docker build -t convergence:latest .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key-here \
  --name convergence \
  convergence:latest
```

### 2. Bare Metal Deployment

#### System Requirements

- Ubuntu 20.04+ or similar Linux distribution.
  Other Linux distributions work but Ubuntu is best tested.
- Python 3.9+.
  Required for modern Python features and type hints.
- 2GB RAM minimum.
  More RAM improves performance for concurrent requests.
- 10GB disk space.
  Includes space for generated audio files and logs.

#### Installation Steps

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip

# Clone and setup
git clone https://github.com/prodigaltech/convergence.git
cd convergence

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install package
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

#### Running as a Service

Create `/etc/systemd/system/convergence.service`:

```ini
[Unit]
Description=Convergence API Service
After=network.target

[Service]
Type=simple
User=convergence
WorkingDirectory=/opt/convergence
Environment="PATH=/opt/convergence/venv/bin"
ExecStart=/opt/convergence/venv/bin/uvicorn convergence.api.app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable convergence
sudo systemctl start convergence
```

### 3. Kubernetes Deployment

#### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: convergence
spec:
  replicas: 2
  selector:
    matchLabels:
      app: convergence
  template:
    metadata:
      labels:
        app: convergence
    spec:
      containers:
      - name: convergence
        image: convergence:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: convergence-secrets
              key: openai-api-key
```

## Configuration

### Environment Variables

Essential variables for self-hosting:

```bash
# Required
OPENAI_API_KEY=your-api-key

# Optional but recommended
ENVIRONMENT=production
LOG_LEVEL=info
MAX_WORKERS=4

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Security Considerations

1. **Use HTTPS**: Deploy behind a reverse proxy (Nginx/Caddy).
   SSL/TLS encryption is essential for protecting API keys in transit.
2. **API Keys**: Enable authentication for production.
   Never expose unauthenticated endpoints to the public internet.
3. **Firewall**: Restrict access to necessary ports only.
   Use cloud security groups or iptables to limit exposure.
4. **Updates**: Keep dependencies updated.
   Regular updates patch security vulnerabilities and improve performance.

### Reverse Proxy Setup (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name convergence.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Monitoring

### Health Checks

```bash
# API health endpoint
curl http://localhost:8000/health

# Authentication status
curl http://localhost:8000/auth/status
```

### Logging

Logs are written to:
- Console (stdout/stderr).
  Standard output makes integration with log aggregation systems easy.
- Optional file logging via LOG_FILE environment variable.
  Enable file logging for persistent log storage and analysis.

### Metrics

Consider adding:
- Prometheus metrics endpoint.
  Track request counts, latencies, and error rates.
- Application Performance Monitoring (APM).
  Gain deep insights into application performance.
- Error tracking (Sentry).
  Catch and fix errors before users report them.

## Scaling

### Horizontal Scaling

- Deploy multiple API instances.
  Scale out to handle increased load across multiple servers.
- Use a load balancer.
  Distribute requests evenly across your instance fleet.
- Share nothing architecture.
  Each instance is independent for maximum reliability.

### Performance Tuning

```bash
# Increase workers for high load
MAX_WORKERS=8

# Adjust timeouts
REQUEST_TIMEOUT=300

# Enable response caching
ENABLE_CACHE=true
CACHE_TTL=3600
```

## Backup and Recovery

### Data to Backup

- Environment configuration.
  Your .env files contain critical settings that must be preserved.
- Generated audio files (if persisted).
  Keep historical conversations if required by your use case.
- API keys database (if using authentication).
  The Google Sheet or database containing your API keys.

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/convergence"
DATE=$(date +%Y%m%d)

# Backup config
cp /opt/convergence/.env $BACKUP_DIR/env-$DATE

# Backup generated files
tar -czf $BACKUP_DIR/audio-$DATE.tar.gz /opt/convergence/output/
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in .env
   API_PORT=8001
   ```
   Common when running multiple services on the same host.

2. **Memory Issues**
   - Increase container/VM memory.
     Audio generation can be memory-intensive for long conversations.
   - Reduce MAX_WORKERS.
     Fewer workers mean lower memory usage but reduced concurrency.

3. **API Key Errors**
   - Verify OPENAI_API_KEY is set.
     Check your environment variables are properly loaded.
   - Check API key permissions.
     Ensure your OpenAI key has the necessary permissions.

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=debug
DEBUG=true
```

## Next Steps

- Configure [API Key Management](API_KEY_MANAGEMENT).
  Secure your API endpoints with robust authentication.
- Set up monitoring and alerts.
  Know about issues before your users do.
- Review [Security](../README#-security) best practices.
  Ensure your deployment follows security guidelines.