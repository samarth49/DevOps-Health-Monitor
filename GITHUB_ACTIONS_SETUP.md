# GitHub Actions CI/CD Setup Guide

This guide walks you through setting up GitHub Actions for the DevOps Health Monitor project.

## Prerequisites

- GitHub repository with the code pushed
- Docker Hub account
- GitHub repository settings access

---

## Step 1: Create Docker Hub Personal Access Token

### Why?
You need authentication credentials to push Docker images to Docker Hub from GitHub Actions.

### Steps:

1. Go to **[Docker Hub Settings](https://hub.docker.com/settings/security)** in your browser
2. Click **"Security"** in the left sidebar
3. Click **"Generate New Token"** button
4. In the dialog:
   - **Token name**: Enter `github-actions`
   - **Access permissions**: Select **"Read & Write"**
5. Click **"Generate"** button
6. **Copy the generated token** (you'll need it in the next step)
   - ⚠️ **Important**: Save this token somewhere safe - Docker Hub won't show it again!

---

## Step 2: Add Docker Credentials to GitHub Secrets

### Why?
GitHub Actions needs your Docker Hub credentials to authenticate and push images.

### Steps:

1. Go to your GitHub repository
2. Click **"Settings"** (top navigation)
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** button
5. Create first secret:
   - **Name**: `DOCKER_USERNAME`
   - **Secret**: Your Docker Hub username
   - Click **"Add secret"**

6. Click **"New repository secret"** again
7. Create second secret:
   - **Name**: `DOCKER_PASSWORD`
   - **Secret**: Paste the token you generated in Step 1
   - Click **"Add secret"**

✅ You should now see both secrets listed:
- `DOCKER_PASSWORD`
- `DOCKER_USERNAME`

---

## Step 3: Verify the Workflow File

The GitHub Actions workflow is already configured at `.github/workflows/ci-cd.yml`

### What the workflow does:

| Stage | Action |
|-------|--------|
| **Checkout** | Pulls your code from the repository |
| **Python Setup** | Installs Python 3.11 |
| **Dependencies** | Creates virtual environment and installs requirements |
| **Tests** | Runs pytest on test_app.py |
| **Docker Setup** | Prepares Docker Buildx for building |
| **Docker Login** | Authenticates with Docker Hub using your secrets |
| **Build & Push** | Builds Docker image and pushes to Docker Hub |
| **Success/Failure** | Posts result message |

---

## Step 4: Trigger Your First Build

GitHub Actions automatically runs the workflow when you push to the `main` branch.

### Option A: Push Changes

```bash
git add .
git commit -m "Setup GitHub Actions CI/CD"
git push origin main
```

### Option B: Manual Trigger

1. Go to your GitHub repository
2. Click **"Actions"** tab (top navigation)
3. Click **"DevOps Health Monitor CI/CD"** workflow
4. Click **"Run workflow"** button
5. Select **"main"** branch
6. Click **"Run workflow"**

---

## Step 5: Monitor Your Build

### View Build Status:

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on the latest workflow run
4. Watch the build progress in real-time

### What to look for:

✅ **Success** (green checkmark):
- All stages passed
- Docker image pushed to Docker Hub
- You can pull and run the image with: `docker pull <USERNAME>/health-monitor:latest`

❌ **Failure** (red X):
- Check the logs for the failing stage
- Common issues:
  - Docker credentials invalid
  - Tests failed
  - Docker socket permissions
  - Python dependency issues

---

## Step 6: Verify Docker Image

Once the build succeeds, verify your Docker image on Docker Hub:

1. Go to **[Docker Hub](https://hub.docker.com)**
2. Log in with your credentials
3. Click on your profile → **Repositories**
4. You should see **`health-monitor`** repository
5. Click on it to view:
   - Image tags (should show `latest`)
   - Build history
   - Last push time

### Pull and Run the Image:

```bash
docker pull <YOUR_DOCKER_USERNAME>/health-monitor:latest
docker run <YOUR_DOCKER_USERNAME>/health-monitor:latest
```

---

## Step 7: Set Up Automatic Triggers (Optional)

### Current Setup

The workflow triggers automatically on:
- ✅ Every push to `main` branch
- ✅ Every pull request to `main` branch

### Customize Triggers

Edit `.github/workflows/ci-cd.yml` to change when workflow runs:

```yaml
on:
  push:
    branches: [ main, develop ]        # Also trigger on develop branch
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'               # Daily at 2 AM UTC
```

---

## Troubleshooting

### Issue: Docker Login Failed (401 Unauthorized)

**Cause**: Invalid Docker Hub credentials

**Fix**:
1. Verify your Docker Hub username and password
2. Go to GitHub → Settings → Secrets
3. Update `DOCKER_PASSWORD` with a fresh Personal Access Token from Docker Hub
4. Trigger a new build

### Issue: Tests Failed

**Cause**: Test files have issues or dependencies are missing

**Fix**:
1. Check the logs in the GitHub Actions UI
2. Look for the "Run Tests" stage
3. Fix the issues locally and push again:
   ```bash
   python -m pytest test_app.py -v
   ```

### Issue: Docker Build Failed

**Cause**: Dockerfile syntax error or missing files

**Fix**:
1. Test building locally:
   ```bash
   docker build -t health-monitor:latest .
   ```
2. Fix any errors
3. Push the changes and let GitHub Actions retry

### Issue: Workflow Not Running

**Cause**: Workflow file is disabled or branch doesn't exist

**Fix**:
1. Go to **Actions** tab → check if workflow is enabled
2. Make sure you're pushing to `main` branch (not `master`)
3. Verify `.github/workflows/ci-cd.yml` file exists

---

## Monitoring Workflow Performance

### View Workflow Runs History

1. Go to **Actions** tab
2. Click **"DevOps Health Monitor CI/CD"**
3. See all previous runs with:
   - Status (✅ or ❌)
   - Timestamp
   - Branch
   - Commit message
   - Duration

### Set Up Notifications (Optional)

GitHub can notify you when workflows fail:
1. Go to **Settings** → **Notifications**
2. Check **"Workflows"**
3. Select notification method (email, etc.)

---

## Advanced: Customize the Workflow

### Add More Branches to Trigger

Edit `.github/workflows/ci-cd.yml`:
```yaml
on:
  push:
    branches: [ main, develop, staging ]
```

### Skip Docker Push on Pull Requests

Add condition to the push step:
```yaml
- name: Build and push Docker image
  if: github.event_name == 'push'
  uses: docker/build-push-action@v4
```

### Add Code Quality Checks

Add before tests:
```yaml
- name: Lint with flake8
  run: |
    source venv/bin/activate
    pip install flake8
    flake8 app.py test_app.py
```

---

## Summary

You now have:
- ✅ Automated testing on every push
- ✅ Automated Docker image building
- ✅ Automated Docker image pushing to Docker Hub
- ✅ CI/CD pipeline that runs in the cloud (no server needed!)

**Enjoy automated deployments! 🚀**
