# Google OAuth2 Authentication Setup Guide

This guide walks you through setting up Google OAuth2 authentication for your ADK application, similar to Azure AD app registration.

## 📝 Overview

The OAuth2 implementation provides:
- **Automatic redirect** to Google Sign-In for unauthenticated users
- **Token validation** and session management
- **Secure access** to your agents and API endpoints
- **Zero code changes** to your existing agents

## 🔑 Step 1: Create Google OAuth2 Application

### 1.1 Go to Google Cloud Console
1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `test-trendspotter-adk`
3. Navigate to **APIs & Services** > **Credentials**

### 1.2 Create OAuth2 Client ID
1. Click **"+ CREATE CREDENTIALS"** > **"OAuth client ID"**
2. If prompted, configure the OAuth consent screen first:
   - **Application type**: Internal (for organization) or External (for any Google user)
   - **Application name**: `Trend Spotter ADK`
   - **User support email**: Your email
   - **Authorized domains**: Your domain (e.g., `yourdomain.com`)
   - **Developer contact**: Your email

### 1.3 Configure OAuth Client
1. **Application type**: Web application
2. **Name**: `Trend Spotter Web App`
3. **Authorized JavaScript origins**:
   - `http://localhost:8080` (for local development)
   - `https://your-cloud-run-url` (for production)
4. **Authorized redirect URIs**:
   - `http://localhost:8080/auth/callback` (for local development)
   - `https://your-cloud-run-url/auth/callback` (for production)
5. Click **"CREATE"**

### 1.4 Download Credentials
1. Copy the **Client ID** and **Client Secret**
2. Keep these secure - you'll add them to environment variables

## 🔐 Step 2: Configure Environment Variables

### 2.1 Local Development (.env file)
The application automatically loads OAuth2 credentials from your `.env` file. Add these lines:

```bash
# Google OAuth2 Configuration
GOOGLE_OAUTH2_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret-here
GOOGLE_OAUTH2_REDIRECT_BASE_URL=http://localhost:8080

# Optional: Custom session secret (auto-generated if not provided)
# SESSION_SECRET_KEY=your-custom-session-secret
```

### 2.2 Production Deployment (GitHub Secrets)
Add these to your GitHub repository secrets:

1. Go to [GitHub Repository Settings > Secrets and Variables > Actions](https://github.com/subhashishd/trend-spotter/settings/secrets/actions)
2. Add new repository secrets:
   - **`GOOGLE_OAUTH2_CLIENT_ID`**: Your OAuth client ID
   - **`GOOGLE_OAUTH2_CLIENT_SECRET`**: Your OAuth client secret
   - **`GOOGLE_OAUTH2_REDIRECT_BASE_URL`**: Your production URL (e.g., `https://your-service-url`)

## 🚀 Step 3: Start Authenticated Server

### 3.1 Local Development
```bash
# Install new dependencies
pip install -r requirements.txt

# Start the authenticated server
python authenticated_server.py
```

### 3.2 Test Authentication Flow
1. Open `http://localhost:8080` in your browser
2. You should be redirected to Google Sign-In
3. After signing in, you'll be redirected back to your app
4. Your app will now be accessible with your Google account

### 3.3 Authentication Endpoints
- **Login**: `/auth/login` - Initiates Google OAuth flow
- **Callback**: `/auth/callback` - Handles Google OAuth callback
- **Logout**: `/auth/logout` - Logs out the user
- **Status**: `/auth/status` - Check authentication status (JSON API)

## 🌐 Step 4: Production Deployment

### 4.1 Update Deployment Scripts
The authentication middleware will automatically be included when:
1. OAuth2 environment variables are set
2. You deploy using the updated deployment configuration

### 4.2 Deploy with Authentication
```bash
# Push changes to trigger deployment
git add .
git commit -m "Add Google OAuth2 authentication"
git push origin main
```

### 4.3 Update Cloud Run Service URL
After deployment:
1. Get your Cloud Run service URL
2. Update the OAuth2 client configuration in Google Cloud Console
3. Add the production URL to **Authorized redirect URIs**

## 🔧 Step 5: Troubleshooting

### Common Issues

#### 5.1 "OAuth client not found" Error
- **Cause**: Client ID or Client Secret is incorrect
- **Solution**: Verify the credentials in Google Cloud Console

#### 5.2 "Redirect URI mismatch" Error
- **Cause**: The redirect URI doesn't match the configured URIs
- **Solution**: Update the Authorized redirect URIs in Google Cloud Console

#### 5.3 "Access blocked" Error
- **Cause**: OAuth consent screen not properly configured
- **Solution**: Complete the OAuth consent screen configuration

#### 5.4 "Authentication failed" in logs
- **Cause**: Token validation failed
- **Solution**: Check if the token is expired or the client configuration is correct

### Debug Commands

```bash
# Check if environment variables are set
echo $GOOGLE_OAUTH2_CLIENT_ID
echo $GOOGLE_OAUTH2_CLIENT_SECRET

# Test authentication status
curl http://localhost:8080/auth/status

# Check server logs for authentication errors
python authenticated_server.py
```

## 🔒 Security Considerations

### Best Practices
1. **Use HTTPS in production** - OAuth2 requires secure connections
2. **Keep secrets secure** - Never commit OAuth credentials to version control
3. **Restrict authorized domains** - Limit to your organization's domain if needed
4. **Regular credential rotation** - Rotate OAuth secrets periodically
5. **Monitor access** - Review OAuth consent and access logs

### OAuth Consent Screen
- **Internal**: Only users in your Google Workspace organization
- **External**: Any Google user (requires verification for production use)

## 🎉 Success Criteria

✅ **Setup Complete** when:
- [ ] Google OAuth2 client created in Google Cloud Console
- [ ] Environment variables configured (local and GitHub secrets)
- [ ] Authenticated server starts without errors
- [ ] Browser redirects to Google Sign-In when accessing app
- [ ] After signing in, app loads successfully
- [ ] Authentication status endpoint returns user information
- [ ] Logout functionality works correctly

## 📚 Additional Resources

- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth2 Best Practices](https://tools.ietf.org/html/draft-ietf-oauth-security-topics)

---

**🎯 Result**: Your ADK application now has Google OAuth2 authentication, providing secure access similar to Azure AD app registration!

