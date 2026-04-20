// CI/CD pipeline definition
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Pulling code from Git..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh 'pytest test_app.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t health-monitor:latest .'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying container..."
                sh 'docker stop health-monitor || true'
                sh 'docker rm health-monitor || true'
                sh 'docker run -d --name health-monitor health-monitor:latest'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline passed! App deployed."
        }
        failure {
            echo "❌ Pipeline failed! Check the logs."
        }
    }
}
