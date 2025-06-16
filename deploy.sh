#!/bin/bash

# ADK Cloud Run Deployment Script
# This script deploys the trend_spotter agent to Google Cloud Run

set -e

# Default values
GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT:-"test-trendspotter-adk"}
GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"trend-spotter-service"}
APP_NAME=${APP_NAME:-"trend-spotter-app"}
AGENT_PATH=${AGENT_PATH:-"./trend_spotter"}

echo "🚀 Starting ADK deployment..."
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Region: $GOOGLE_CLOUD_LOCATION"
echo "Service: $SERVICE_NAME"
echo "App: $APP_NAME"
echo "Agent Path: $AGENT_PATH"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed or not in PATH"
    echo "Please install Google Cloud CLI: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: No active gcloud authentication found"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Check if project exists and user has access
if ! gcloud projects describe "$GOOGLE_CLOUD_PROJECT" &> /dev/null; then
    echo "❌ Error: Cannot access project $GOOGLE_CLOUD_PROJECT"
    echo "Please check if the project exists and you have access"
    exit 1
fi

# Set the project
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Activate virtual environment and run deployment
echo "📦 Activating virtual environment and deploying..."
source myenv/bin/activate

adk deploy cloud_run \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="$GOOGLE_CLOUD_LOCATION" \
  --service_name="$SERVICE_NAME" \
  --app_name="$APP_NAME" \
  --with_ui \
  "$AGENT_PATH"

echo "✅ Deployment completed!"
echo "Your app should be available at the Cloud Run service URL."

