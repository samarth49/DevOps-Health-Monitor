# DevOps Health Monitor
devops-health-monitor/
├── app.py                 ← Python health check app
├── test_app.py            ← Unit tests
├── requirements.txt       ← Python dependencies
├── Dockerfile             ← Containerize the app
├── Jenkinsfile            ← CI/CD pipeline definition
└── README.md

# Start Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Get the initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

install python & pip into the jenkins container
docker exec -u 0 jenkins apt-get update ; docker exec -u 0 jenkins apt-get install -y python3 python3-pip