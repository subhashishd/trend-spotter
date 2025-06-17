# Production Deployment Checklist

This checklist ensures your multi-agent trend spotter is properly deployed to Google Cloud Run with all necessary secrets configured.

## ✅ Pre-Deployment Verification

Run the verification script first:
```bash
python verify_production_setup.py
```

## 🔐 GitHub Secrets Configuration

### Required Secrets
Go to [GitHub Repository Settings → Secrets and Variables → Actions](https://github.com/subhashishd/trend-spotter/settings/secrets/actions) and add:

#### 1. Google Cloud Authentication
- **GCP_SERVICE_ACCOUNT_KEY**: JSON service account key with Cloud Run deployment permissions
- **GOOGLE_CLOUD_PROJECT**: `test-trendspotter-adk`
- **GOOGLE_CLOUD_LOCATION**: `us-central1` (optional, defaults to us-central1)

#### 2. Reddit API Credentials (Required for Reddit Agent)
**⚠️ Without these, the Reddit agent will not function!**

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill out the form:
   - **Name**: `trend-spotter`
   - **App type**: `script`
   - **Description**: `AI agent for trend spotting on The Agent Factory podcast`
   - **About URL**: (leave blank)
   - **Redirect URI**: `http://localhost:8080`
4. Click "Create app"
5. Add to GitHub secrets:
   - **REDDIT_CLIENT_ID**: The client ID shown under your app name
   - **REDDIT_CLIENT_SECRET**: The secret shown in your app
   - **REDDIT_USER_AGENT**: `trend-spotter:v1.2 (by /u/yourusername)` (replace with your Reddit username)

#### 3. Email Agent Configuration (Required for Email Delivery)
**⚠️ Without these, the Email agent will not function!**

1. Set up Gmail App Password:
   - Go to [Google Account Settings → Security → 2-Step Verification → App passwords](https://myaccount.google.com/apppasswords)
   - Generate an app password for "Mail"
2. Add to GitHub secrets:
   - **SENDER_EMAIL**: Your Gmail address (e.g., `your-email@gmail.com`)
   - **SENDER_APP_PASSWORD**: The app password generated above
   - **EMAIL_RECIPIENTS**: Comma-separated list of recipients (optional, defaults to `tinks70@gmail.com`)
   - **SMTP_SERVER**: `smtp.gmail.com` (optional, defaults to this)
   - **SMTP_PORT**: `587` (optional, defaults to this)

#### 4. Optional Deployment Configuration
- **SERVICE_NAME**: `trend-spotter-service` (optional, defaults to this)
- **APP_NAME**: `trend-spotter-app` (optional, defaults to this)

## 🚀 Deployment Options

### Option 1: Automatic Deployment (Recommended)
```bash
# Commit and push to trigger automatic deployment
git add .
git commit -m "Deploy multi-agent system to production"
git push origin main
```

### Option 2: Manual Deployment via GitHub Actions
1. Go to [GitHub Actions](https://github.com/subhashishd/trend-spotter/actions)
2. Click "Deploy ADK Agent" workflow
3. Click "Run workflow"
4. Select environment: `production`
5. Click "Run workflow"

### Option 3: Local Deployment
```bash
# Make sure you're authenticated with gcloud
gcloud auth login

# Run the deployment script
./deploy.sh
```

## 🔍 Post-Deployment Verification

### 1. Check Deployment Status
- Monitor the GitHub Actions workflow logs
- Verify the Cloud Run service is created and running

### 2. Access the Deployed Application
After successful deployment, your service will be available at:
- **Service URL**: `https://trend-spotter-service-<hash>.<region>.run.app/`
- **Development UI**: `https://trend-spotter-service-<hash>.<region>.run.app/dev-ui/`

### 3. Test the Multi-Agent System
1. Open the Development UI
2. Test with a query like: "What are the latest AI agent trends?"
3. Verify both Google Search and Reddit agents are working:
   - Check that Google Search agent retrieves recent news
   - Verify Reddit agent fetches posts from subreddits
   - Confirm orchestrator synthesizes information from both agents

### 4. Monitor Logs
```bash
# View Cloud Run logs
gcloud logs read --service=trend-spotter-service --region=us-central1 --limit=50
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Reddit Agent Not Working
- **Error**: "Error searching Reddit: ..."
- **Solution**: Verify Reddit API credentials are correctly set in GitHub secrets
- **Check**: Ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are all configured

#### 2. Google Search Agent Issues
- **Error**: Search results not found or limited
- **Solution**: The Google Search agent uses Vertex AI search capabilities by default
- **Check**: Ensure GOOGLE_GENAI_USE_VERTEXAI=true and proper GCP authentication

#### 3. Deployment Failures
- **Error**: "Cannot access project"
- **Solution**: Verify GCP_SERVICE_ACCOUNT_KEY has proper permissions
- **Required roles**:
  - Cloud Run Admin
  - Cloud Build Editor
  - Service Account User
  - Vertex AI User

#### 4. Environment Variable Issues
- **Error**: Missing environment variables in Cloud Run
- **Solution**: Check that all `--env` flags are properly set in the deployment command
- **Verify**: The CI/CD pipeline passes all required environment variables

### Debug Commands

```bash
# Check Cloud Run service status
gcloud run services describe trend-spotter-service --region=us-central1

# View recent deployments
gcloud run revisions list --service=trend-spotter-service --region=us-central1

# Check environment variables in Cloud Run
gcloud run services describe trend-spotter-service --region=us-central1 --format="value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)"
```

## 📊 Performance Monitoring

### Key Metrics to Monitor
- **Response Time**: Agent orchestration should complete within 30-60 seconds
- **Success Rate**: Both Google Search and Reddit agents should have >95% success rate
- **Cost**: Monitor Vertex AI API usage and Cloud Run costs

### Setting Up Alerts
```bash
# Create alerting policy for failed requests
gcloud alpha monitoring policies create --policy-from-file=monitoring-policy.yaml
```

## 🔄 Updates and Maintenance

### Updating the Deployment
1. Make changes to your code
2. Test locally with `adk web --port 8080`
3. Commit and push to trigger automatic deployment
4. Monitor deployment in GitHub Actions

### Rollback if Needed
```bash
# List previous revisions
gcloud run revisions list --service=trend-spotter-service --region=us-central1

# Rollback to previous revision
gcloud run services update-traffic trend-spotter-service --to-revisions=REVISION_NAME=100 --region=us-central1
```

## 🎯 Success Criteria

✅ **Deployment Complete** when:
- [ ] GitHub Actions deployment workflow completes successfully
- [ ] Cloud Run service is running and accessible
- [ ] Development UI loads without errors
- [ ] Test query returns structured intelligence report
- [ ] Both Google Search and Reddit agents contribute to the report
- [ ] Report follows the specified format with trends, releases, and questions

---

**🎉 Congratulations!** Your multi-agent trend spotter is now running in production and ready to generate intelligence reports for "The Agent Factory" podcast!

