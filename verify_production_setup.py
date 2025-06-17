#!/usr/bin/env python3
"""
Production Deployment Verification Script

This script verifies that all required secrets and configurations are properly
set up for production deployment to Google Cloud Run.
"""

import os
import subprocess
from pathlib import Path
from typing import List


class ProductionVerifier:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_messages = []

    def verify_environment_variables(self) -> bool:
        """Verify required environment variables for production."""
        print("🔍 Verifying environment variables...")

        required_vars = {
            "GOOGLE_CLOUD_PROJECT": "Google Cloud project ID",
            "GOOGLE_CLOUD_LOCATION": "Google Cloud region",
            "GOOGLE_GENAI_USE_VERTEXAI": (
                "Use Vertex AI instead of direct Gemini API"
            ),
        }

        optional_reddit_vars = {
            "REDDIT_CLIENT_ID": "Reddit API client ID",
            "REDDIT_CLIENT_SECRET": "Reddit API client secret",
            "REDDIT_USER_AGENT": "Reddit API user agent",
        }

        # Check required variables
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value:
                self.success_messages.append(f"   ✅ {var}: {description}")
            else:
                self.errors.append(f"   ❌ Missing {var}: {description}")

        # Check Reddit variables (optional but recommended)
        reddit_vars_present = 0
        for var, description in optional_reddit_vars.items():
            value = os.getenv(var)
            if value:
                self.success_messages.append(f"   ✅ {var}: {description}")
                reddit_vars_present += 1
            else:
                self.warnings.append(f"   ⚠️  Missing {var}: {description}")

        if reddit_vars_present == 0:
            self.errors.append(
                "   ❌ No Reddit API credentials found - "
                "Reddit agent will not work"
            )
        elif reddit_vars_present < 3:
            self.warnings.append(
                "   ⚠️  Incomplete Reddit API credentials - "
                "some features may not work"
            )

        return len([e for e in self.errors if "reddit" not in e.lower()]) == 0

    def verify_gcloud_setup(self) -> bool:
        """Verify Google Cloud CLI setup."""
        print("\n🔍 Verifying Google Cloud CLI setup...")

        # Check if gcloud is installed
        try:
            result = subprocess.run(
                ["gcloud", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.success_messages.append(
                f"   ✅ Google Cloud CLI installed: {result.stdout.split()[3]}"
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.errors.append("   ❌ Google Cloud CLI not installed")
            return False

        # Check authentication
        try:
            result = subprocess.run(
                [
                    "gcloud",
                    "auth",
                    "list",
                    "--filter=status:ACTIVE",
                    "--format=value(account)",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout.strip():
                self.success_messages.append(
                    f"   ✅ Authenticated as: {result.stdout.strip()}"
                )
            else:
                self.errors.append("   ❌ No active gcloud authentication")
                return False
        except subprocess.CalledProcessError:
            self.errors.append("   ❌ Failed to check gcloud authentication")
            return False

        # Check project access
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id:
            try:
                subprocess.run(
                    ["gcloud", "projects", "describe", project_id],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.success_messages.append(
                    f"   ✅ Can access project: {project_id}"
                )
            except subprocess.CalledProcessError:
                self.errors.append(
                    f"   ❌ Cannot access project: {project_id}"
                )
                return False

        return True

    def verify_github_secrets_documented(self) -> bool:
        """Verify GitHub secrets documentation exists."""
        print("\n🔍 Verifying GitHub secrets documentation...")

        secrets_doc = Path("GITHUB_SECRETS_SETUP.md")
        if secrets_doc.exists():
            self.success_messages.append(
                "   ✅ GitHub secrets setup documentation exists"
            )
            return True
        else:
            self.warnings.append(
                "   ⚠️  GitHub secrets setup documentation missing"
            )
            return False

    def verify_deployment_pipelines(self) -> bool:
        """Verify CI/CD pipeline configurations."""
        print("\n🔍 Verifying deployment pipelines...")

        pipeline_files = {
            ".github/workflows/ci.yml": "Main CI/CD pipeline",
            ".github/workflows/deploy-adk.yml": "ADK deployment pipeline",
            "deploy.sh": "Local deployment script",
        }

        all_exist = True
        for file_path, description in pipeline_files.items():
            if Path(file_path).exists():
                self.success_messages.append(
                    f"   ✅ {description}: {file_path}"
                )
            else:
                self.errors.append(f"   ❌ Missing {description}: {file_path}")
                all_exist = False

        return all_exist

    def verify_adk_installation(self) -> bool:
        """Verify ADK installation and functionality."""
        print("\n🔍 Verifying ADK installation...")

        try:
            result = subprocess.run(
                ["adk", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.success_messages.append(
                f"   ✅ ADK installed: {result.stdout.strip()}"
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.errors.append("   ❌ ADK not installed or not in PATH")
            return False

        # Check if agent can be discovered
        try:
            from trend_spotter.agent import root_agent

            self.success_messages.append(
                f"   ✅ Agent discoverable: {root_agent.name}"
            )
        except ImportError as e:
            self.errors.append(f"   ❌ Cannot import agent: {e}")
            return False

        return True

    def verify_required_apis_enabled(self) -> bool:
        """Verify required Google Cloud APIs are enabled."""
        print("\n🔍 Verifying required Google Cloud APIs...")

        required_apis = [
            "aiplatform.googleapis.com",
            "cloudbuild.googleapis.com",
            "run.googleapis.com",
            "containerregistry.googleapis.com",
        ]

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            self.errors.append("   ❌ GOOGLE_CLOUD_PROJECT not set")
            return False

        all_enabled = True
        for api in required_apis:
            try:
                result = subprocess.run(
                    [
                        "gcloud",
                        "services",
                        "list",
                        "--enabled",
                        f"--filter=name:{api}",
                        "--format=value(name)",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                if result.stdout.strip():
                    self.success_messages.append(f"   ✅ API enabled: {api}")
                else:
                    self.warnings.append(f"   ⚠️  API not enabled: {api}")
                    all_enabled = False
            except subprocess.CalledProcessError:
                self.warnings.append(f"   ⚠️  Cannot check API status: {api}")

        return all_enabled

    def generate_secrets_setup_commands(self) -> List[str]:
        """Generate commands to set up missing secrets."""
        commands = []

        # Reddit API setup
        if not all(
            os.getenv(var)
            for var in [
                "REDDIT_CLIENT_ID",
                "REDDIT_CLIENT_SECRET",
                "REDDIT_USER_AGENT",
            ]
        ):
            commands.extend(
                [
                    "# Set up Reddit API credentials:",
                    "# 1. Go to https://www.reddit.com/prefs/apps",
                    "# 2. Create a new 'script' application",
                    "# 3. Note down the client ID and secret",
                    "# 4. Add to GitHub secrets:",
                    "#    REDDIT_CLIENT_ID=<your_client_id>",
                    "#    REDDIT_CLIENT_SECRET=<your_client_secret>",
                    "#    REDDIT_USER_AGENT=trend-spotter:v1.0 "
                    "(by /u/yourusername)",
                    "",
                ]
            )

        return commands

    def run_verification(self) -> bool:
        """Run all verification checks."""
        print("🚀 Starting Production Deployment Verification\n")
        print("=" * 60)

        checks = [
            self.verify_environment_variables,
            self.verify_gcloud_setup,
            self.verify_adk_installation,
            self.verify_deployment_pipelines,
            self.verify_github_secrets_documented,
            self.verify_required_apis_enabled,
        ]

        all_passed = True
        for check in checks:
            if not check():
                all_passed = False

        print("\n" + "=" * 60)
        print("📋 VERIFICATION SUMMARY")
        print("=" * 60)

        if self.success_messages:
            print("\n✅ SUCCESSFUL CHECKS:")
            for msg in self.success_messages:
                print(msg)

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(warning)

        if self.errors:
            print("\n❌ ERRORS TO FIX:")
            for error in self.errors:
                print(error)

        setup_commands = self.generate_secrets_setup_commands()
        if setup_commands:
            print("\n🔧 SETUP COMMANDS:")
            for cmd in setup_commands:
                print(cmd)

        print("\n" + "=" * 60)
        if all_passed and not self.errors:
            print("🎉 ALL CHECKS PASSED! Ready for production deployment.")
            print("\n📝 Next steps:")
            print("   1. Ensure all GitHub secrets are configured")
            print("   2. Run: git push origin main (to trigger deployment)")
            print(
                "   3. Or manually trigger: GitHub Actions → Deploy ADK Agent"
            )
        else:
            print("❌ VERIFICATION FAILED! Please fix the errors above.")
            print("\n📝 Required actions:")
            if self.errors:
                print("   1. Fix all error conditions listed above")
            if self.warnings:
                print(
                    "   2. Address warning conditions for full functionality"
                )
            print("   3. Re-run this verification script")

        print("=" * 60)
        return all_passed and not self.errors


def main():
    """Main verification function."""
    # Load environment variables from .env file if it exists
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

    verifier = ProductionVerifier()
    success = verifier.run_verification()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
