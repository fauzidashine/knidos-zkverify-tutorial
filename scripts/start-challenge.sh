#!/bin/bash
# Knidos zkVerify Challenge — Quick Start
# Run this script to start the challenge container with proper tunnel
# Usage: ./start-challenge.sh

set -e

echo "🚀 Starting Knidos zkVerify Challenge..."
echo

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker daemon
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon not running. Start Docker Desktop first."
    exit 1
fi

# Stop any existing container
echo "🧹 Cleaning up old containers..."
docker stop knidos_run 2>/dev/null || true
docker rm -f knidos_run 2>/dev/null || true

# Start challenge container
echo "📦 Pulling & starting challenge image..."
docker run --pull=always -it \
    --name knidos_run \
    -p 7878:7878 \
    ghcr.io/node101-io/knidos-challenge:latest

echo
echo "✅ Container started!"
echo
echo "👉 Next steps:"
echo "   1. Open http://localhost:7878 in your browser"
echo "   2. Connect wallet (MetaMask/Rabby)"
echo "   3. Sign the message"
echo "   4. Come back here — follow terminal prompts"
echo
