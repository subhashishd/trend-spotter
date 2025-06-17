# Deployment Guide

This guide explains how to deploy the Trend Spotter ADK agent to Google Cloud Run.

## Prerequisites

### 1. Google Cloud Setup

1. **Install Google Cloud CLI**
   ```bash
   # For macOS
   brew install --cask google-cloud-sdk
   
   # For other platforms, see: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Create or verify Google Cloud Project**
   ```bash
   # Create a new project (if needed)
   gcloud projects create test-trendspotter-adk --name="Trend Spotter ADK"
   
   # Set the project
   gcloud config set project test-trendspotter-adk
   
   # Enable billing (required for Cloud Run)
   # This must be done through the Google Cloud Console
   ```

4. **Enable Required APIs**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

### 2. Environment Variables

Set the following environment variables:

```bash
export GOOGLE_CLOUD_PROJECT="test-trendspotter-adk"
export GOOGLE_CLOUD_LOCATION="us-central1"
export SERVICE_NAME="trend-spotter-service"
export APP_NAME="trend-spotter-app"
export AGENT_PATH="./trend_spotter"
```

## Local Deployment

### Option 1: Using the Deployment Script

```bash
# Make sure you're in the project directory
cd /path/to/trend_spotter

# Run the deployment script
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# Activate virtual environment
source myenv/bin/activate

# Deploy using ADK
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=$SERVICE_NAME \
  --app_name=$APP_NAME \
  --with_ui \
  $AGENT_PATH
```

## GitHub Actions Deployment

### Required GitHub Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and variables > Actions):

1. **`GCP_SERVICE_ACCOUNT_KEY`** (Required)
   - Create a service account in Google Cloud
   - Grant necessary roles (Cloud Run Admin, Cloud Build Service Account, Storage Admin)
   - Download the JSON key file
   - Copy the entire JSON content as the secret value

2. **`GOOGLE_CLOUD_PROJECT`** (Required)
   - Value: `test-trendspotter-adk`

3. **`GOOGLE_CLOUD_LOCATION`** (Optional)
   - Value: `us-central1` (default if not set)

4. **`SERVICE_NAME`** (Optional)
   - Value: `trend-spotter-service` (default if not set)

5. **`APP_NAME`** (Optional)
   - Value: `trend-spotter-app` (default if not set)

### Service Account Setup

1. Create a service account:
   ```bash
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions Service Account"
   ```

2. Grant necessary roles:
   ```bash
   PROJECT_ID="test-trendspotter-adk"
   SERVICE_ACCOUNT="github-actions@${PROJECT_ID}.iam.gserviceaccount.com"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$SERVICE_ACCOUNT" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$SERVICE_ACCOUNT" \
     --role="roles/cloudbuild.builds.builder"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$SERVICE_ACCOUNT" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$SERVICE_ACCOUNT" \
     --role="roles/iam.serviceAccountUser"
   ```

3. Download the key file:
   ```bash
   gcloud iam service-accounts keys create github-actions-key.json \
     --iam-account=$SERVICE_ACCOUNT
   ```

4. Copy the content of `github-actions-key.json` and add it as the `GCP_SERVICE_ACCOUNT_KEY` secret in GitHub.

### Deployment Workflows

The project includes two deployment workflows:

1. **Continuous Deployment (CI)**: Automatically deploys on push to main branch
2. **Manual Deployment (ADK)**: Can be triggered manually with environment selection

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure the service account has the required roles
   - Verify project billing is enabled

2. **API Not Enabled**
   - Run the enable APIs commands listed above

3. **Authentication Issues**
   - Check if gcloud auth is working: `gcloud auth list`
   - For GitHub Actions, verify the service account key is valid

4. **Project Not Found**
   - Verify the project ID is correct
   - Ensure you have access to the project

### Verification

After deployment:

1. **Check Cloud Run service**:
   ```bash
   gcloud run services list --region=$GOOGLE_CLOUD_LOCATION
   ```

2. **Get service URL**:
   ```bash
   gcloud run services describe $SERVICE_NAME \
     --region=$GOOGLE_CLOUD_LOCATION \
     --format="value(status.url)"
   ```

3. **Test the deployed service**:
   ```bash
   curl -X GET "https://YOUR_SERVICE_URL/health"
   ```

## Costs

Google Cloud Run pricing:
- **CPU**: $0.0000024 per vCPU-second
- **Memory**: $0.0000025 per GiB-second
- **Requests**: $0.40 per million requests
- **Free tier**: 2 million requests per month

For development/testing, costs should be minimal.

## Security

- Service is deployed with authentication required by default
- Use IAM policies to control access
- Consider VPC connectivity for production deployments
- Regularly rotate service account keys

