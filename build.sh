#!/bin/bash

IMAGE_NAME="my_api"
TAG=$(date +%Y%m%d-%H%M%S)

# Zapiš tag do .env pro docker-compose
echo "IMAGE_TAG=$TAG" > .env

echo "Buildím image: $IMAGE_NAME:$TAG"
docker-compose build

echo "Spouštím container..."
docker-compose up -d

echo "✅ Hotovo: $IMAGE_NAME:$TAG běží přes Docker Compose"
