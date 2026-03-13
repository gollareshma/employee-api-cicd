pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/gollareshma/employee-api-cicd.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Start API & Run Tests') {
            steps {
                sh '''#!/bin/bash
                . venv/bin/activate

                echo "Starting Flask API..."
                nohup python app.py > server.log 2>&1 &
                APP_PID=$!
                echo "Flask PID: $APP_PID"

                echo "Waiting for API to become ready..."
                for i in {1..20}; do
                    if curl -s http://127.0.0.1:5000/health > /dev/null; then
                        echo "API is ready!"
                        break
                    fi
                    echo "Attempt $i: not ready yet..."
                    sleep 2
                done

                echo "Running tests..."
                pytest tests/ -v
                TEST_EXIT=$?

                echo "Stopping API..."
                kill $APP_PID || true

                exit $TEST_EXIT
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t employee-api .'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}