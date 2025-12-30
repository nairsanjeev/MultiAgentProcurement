#!/bin/bash
# Azure App Service startup script for Next.js

echo "Installing dependencies..."
npm ci --only=production

echo "Starting Next.js production server on port 8080..."
npm run start
