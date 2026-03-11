# Multi-stage build for smaller final image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies (Nginx + curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy app code
COPY app/ ./app/

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Create nginx cache directories with proper permissions
RUN mkdir -p /var/cache/nginx/client_temp \
    && mkdir -p /var/log/nginx \
    && chmod -R 755 /var/cache/nginx \
    && chmod -R 755 /var/log/nginx

# Expose port 80 (Nginx listens here)
EXPOSE 80

# Health check optimized for ECS
# ECS has its own health checks, but this helps during local testing
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start Nginx + Uvicorn together
CMD ["/start.sh"]
