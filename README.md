# DevOps Health Monitor

A Python application that monitors the health status of URLs. Includes comprehensive CI/CD setup with both Jenkins and GitHub Actions.

## Project Structure

```
devops-health-monitor/
├── app.py                      ← Python health check app
├── test_app.py                 ← Unit tests
├── requirements.txt            ← Python dependencies
├── Dockerfile                  ← Containerize the app
├── Jenkinsfile                 ← Jenkins CI/CD pipeline
├── .github/workflows/ci-cd.yml ← GitHub Actions workflow
└── README.md
```

## Option 1: Jenkins CI/CD Setup

### Step 1: Start Jenkins Container

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### Step 2: Get Initial Admin Password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Access Jenkins at `http://localhost:8080` and log in with the password.

### Step 3: Install Required Tools in Jenkins Container

Get your container ID:
```bash
docker ps
```

Install Python3, venv, and Docker CLI:
```bash
docker exec -u 0 <CONTAINER_ID> bash -c "apt-get update && apt-get install -y python3 python3-venv docker.io"
```

Example:
```bash
docker exec -u 0 1d2fded47074 bash -c "apt-get update && apt-get install -y python3 python3-venv docker.io"
```

Fix Docker socket permissions:
```bash
docker exec -u 0 <CONTAINER_ID> chmod 666 /var/run/docker.sock
```

Restart Jenkins:
```bash
docker restart <CONTAINER_ID>
```

### Step 4: Create Jenkins Pipeline Job

1. Click **"New Item"** in Jenkins UI
2. Enter job name: `DevOps-Health-Monitor`
3. Select **"Pipeline"** and click **"OK"**
4. Under **"Pipeline"** section:
   - Select **"Pipeline script from SCM"**
   - Choose **"Git"** as SCM
   - Enter repository URL: `https://github.com/samarth49/DevOps-Health-Monitor.git`
   - Script path: `Jenkinsfile`
5. Click **"Save"** and **"Build Now"**

### Jenkins Pipeline Stages

- ✅ Checkout code from Git
- ✅ Install Python dependencies
- ✅ Run unit tests with pytest
- ✅ Build Docker image
- ✅ Deploy container

---

## Option 2: GitHub Actions CI/CD Setup (Recommended)

### Step 1: Add Docker Hub Credentials

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add two secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

### Step 2: The Workflow File

The workflow is already configured in `.github/workflows/ci-cd.yml`. It automatically triggers on every push to the `main` branch.

### Step 3: Deploy

Just commit and push:
```bash
git add .
git commit -m "Add GitHub Actions CI/CD"
git push
```

GitHub will automatically run the workflow. Check the **Actions** tab in your GitHub repo to see the build status.

### GitHub Actions Pipeline Stages

- ✅ Checkout code
- ✅ Set up Python 3.11
- ✅ Install dependencies with venv
- ✅ Run tests with pytest
- ✅ Build Docker image
- ✅ Push to Docker Hub

---

## Running Locally

```bash
# Create virtual environment
python -m venv venv

# Activate venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test_app.py -v

# Run the app
python app.py
```

## Building Docker Image

```bash
docker build -t health-monitor:latest .
docker run -d --name health-monitor health-monitor:latest
```

## Troubleshooting

**Jenkins: `docker: not found`**
- Run: `docker exec -u 0 <CONTAINER_ID> apt-get install -y docker.io`

**Jenkins: Python venv error**
- Run: `docker exec -u 0 <CONTAINER_ID> apt-get install -y python3-venv`

**Jenkins: PEP 668 error**
- Already fixed in Jenkinsfile by using virtual environments

**GitHub Actions: Docker push fails**
- Ensure `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set correctly