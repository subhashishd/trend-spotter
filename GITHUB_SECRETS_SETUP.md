# GitHub Secrets Setup Guide

This guide explains how to set up GitHub secrets for automated ADK deployment.

## Required Secrets

You need to set up the following secrets in your GitHub repository:

### 1. GCP_SERVICE_ACCOUNT_KEY
**Description:** The JSON key for your Google Cloud service account  
**How to get it:**
```bash
# Export your current service account key (if you have one)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
cat "$GOOGLE_APPLICATION_CREDENTIALS"

# OR create a new service account key
gcloud iam service-accounts create github-actions-sa --display-name="GitHub Actions Service Account"
gcloud projects add-iam-policy-binding test-trendspotter-adk --member="serviceAccount:github-actions-sa@test-trendspotter-adk.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding test-trendspotter-adk --member="serviceAccount:github-actions-sa@test-trendspotter-adk.iam.gserviceaccount.com" --role="roles/cloudbuild.builds.editor"
gcloud projects add-iam-policy-binding test-trendspotter-adk --member="serviceAccount:github-actions-sa@test-trendspotter-adk.iam.gserviceaccount.com" --role="roles/iam.serviceAccountUser"
gcloud iam service-accounts keys create github-actions-key.json --iam-account=github-actions-sa@test-trendspotter-adk.iam.gserviceaccount.com
cat github-actions-key.json
```

### 2. GOOGLE_CLOUD_PROJECT
**Value:** `test-trendspotter-adk`  
**Description:** Your Google Cloud project ID

### 3. GOOGLE_CLOUD_LOCATION (Optional)
**Value:** `us-central1`  
**Description:** The region where you want to deploy (defaults to us-central1)

### 4. SERVICE_NAME (Optional)
**Value:** `trend-spotter-service`  
**Description:** The name of the Cloud Run service (defaults to trend-spotter-service)

### 5. APP_NAME (Optional)
**Value:** `trend-spotter-app`  
**Description:** The name of the ADK app (defaults to trend-spotter-app)

## How to Add Secrets to GitHub

1. Go to your repository: https://github.com/subhashishd/trend-spotter
2. Click on **Settings** tab
3. Click on **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret one by one:

### Setting up GCP_SERVICE_ACCOUNT_KEY:
- **Name:** `GCP_SERVICE_ACCOUNT_KEY`
- **Value:** The entire JSON content from your service account key file

### Setting up other secrets:
- **GOOGLE_CLOUD_PROJECT:** `test-trendspotter-adk`
- **GOOGLE_CLOUD_LOCATION:** `us-central1`
- **SERVICE_NAME:** `trend-spotter-service`
- **APP_NAME:** `trend-spotter-app`

## Testing the Automated Deployment

Once secrets are set up, you can test deployment by:

1. **Manual trigger:** Go to Actions → Deploy ADK Agent → Run workflow
2. **Automatic trigger:** Push to main branch or create a tag

## Deployment URLs

After successful deployment, your service will be available at:
- **Service URL:** https://trend-spotter-service-1009486516969.us-central1.run.app/
- **Development UI:** https://trend-spotter-service-1009486516969.us-central1.run.app/dev-ui/

## Troubleshooting

If deployment fails:
1. Check the Actions log for detailed error messages
2. Verify all secrets are set correctly
3. Ensure the service account has the required permissions
4. Check that the Google Cloud APIs are enabled

## Security Notes

- Never commit service account keys to your repository
- Use GitHub secrets for all sensitive information
- Regularly rotate service account keys
- Use least privilege principles for service account permissions

