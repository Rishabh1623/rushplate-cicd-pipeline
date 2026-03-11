#!/bin/bash
set -e

echo "Starting RushPlate..."

# Start Uvicorn in background
echo "Starting Uvicorn on port 8000..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

UVICORN_PID=$!

# Wait for Uvicorn to be ready
echo "Waiting for Uvicorn to be ready..."
for i in {1..10}; do
    if curl -s http://127.0.0.1:8000/health > /dev/null; then
        echo "Uvicorn is ready!"
        break
    fi
    echo "Waiting... ($i/10)"
    sleep 2
done

# Start Nginx in foreground (keeps container alive)
echo "Starting Nginx on port 80..."
nginx -g "daemon off;"
