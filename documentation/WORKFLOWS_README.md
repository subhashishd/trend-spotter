# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Trend Spotter project.

## Workflows Overview

### 1. CI/CD Pipeline (`ci.yml`)
Comprehensive CI/CD pipeline that runs on pushes and pull requests.

**Features:**
- **Testing & Linting**: Runs pytest, flake8, black, and mypy
- **Security Scanning**: Uses safety and bandit for vulnerability detection
- **Package Building**: Builds Python packages
- **Integration Testing**: Runs integration tests on main branch
- **Deployment**: Automated deployment to production

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual dispatch

### 2. ADK Deployment (`deploy-adk.yml`)
Specialized workflow for deploying Google ADK agents.

**Features:**
- Google Cloud authentication
- ADK agent deployment
- Post-deployment verification
- Environment-specific deployments

**Triggers:**
- Push to `main` branch
- Git tags starting with `v`
- Manual dispatch with environment selection

### 3. Code Quality (`code-quality.yml`)
Lightweight code quality checks for quick feedback.

**Features:**
- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)
- Security scanning (bandit)

**Triggers:**
- Pull requests to `main` or `develop`
- Push to `main` or `develop`

## Setup Instructions

### Required Secrets
Add these secrets to your GitHub repository settings:

#### For ADK Deployment:
- `GCP_PROJECT_ID`: Your Google Cloud Project ID
- `GCP_SERVICE_ACCOUNT_KEY`: Service account JSON key with necessary permissions
- `GCP_REGION`: (Optional) Deployment region, defaults to `us-central1`

#### For Full CI/CD:
All ADK secrets plus any additional deployment-specific credentials.

### Service Account Permissions
Your GCP service account should have these IAM roles:
- `AI Platform Developer` (for Vertex AI)
- `Cloud Run Developer` (if deploying to Cloud Run)
- `Storage Admin` (for artifact storage)
- `Service Account User`

### Environment Setup

1. **Create GitHub Environments:**
   - Go to Settings → Environments
   - Create `staging` and `production` environments
   - Add protection rules as needed

2. **Configure Branch Protection:**
   - Require status checks to pass
   - Require branches to be up to date
   - Include administrators in restrictions

3. **Enable Dependency Updates:**
   - Consider adding Dependabot configuration
   - Set up security alerts

## Workflow Customization

### Modifying Python Version
Update the `PYTHON_VERSION` environment variable in each workflow.

### Adding New Tests
Tests are automatically discovered by pytest. Add test files following the `test_*.py` pattern.

### Customizing Deployment
Modify the deployment steps in `ci.yml` and `deploy-adk.yml` based on your infrastructure:

- **Google Cloud Run**: Add container building and deployment steps
- **PyPI Publishing**: Add PyPI token and publishing steps
- **Custom Infrastructure**: Add your specific deployment commands

### ADK-Specific Configuration
Update the ADK deployment commands in `deploy-adk.yml`:

```yaml
- name: Deploy ADK Agent
  run: |
    # Your specific ADK deployment commands
    adk deploy --project=${{ env.PROJECT_ID }} \
               --region=${{ env.REGION }} \
               --agent=trend_spotter
```

## Monitoring and Troubleshooting

### Viewing Workflow Runs
- Go to the "Actions" tab in your GitHub repository
- Click on any workflow run to see detailed logs
- Download artifacts for debugging

### Common Issues

1. **Authentication Failures**: Check that secrets are properly set
2. **Test Failures**: Review test logs and fix failing tests
3. **Linting Errors**: Run formatters locally before committing
4. **Deployment Issues**: Verify GCP permissions and project settings

### Local Development
Run the same checks locally:

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run formatters
black .
isort .

# Run linters
flake8 .
mypy . --ignore-missing-imports

# Run tests
pytest -v

# Security checks
bandit -r .
safety check
```

## Best Practices

1. **Keep workflows fast**: Use caching and parallel jobs
2. **Security first**: Never commit secrets, use GitHub secrets
3. **Environment parity**: Keep staging and production similar
4. **Rollback strategy**: Implement deployment rollback procedures
5. **Monitoring**: Set up alerts for failed deployments

## Contributing

When modifying workflows:
1. Test changes in a fork first
2. Use semantic commit messages
3. Update this documentation
4. Consider backward compatibility

