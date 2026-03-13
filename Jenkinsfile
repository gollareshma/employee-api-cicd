pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
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

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate

                echo "Starting Flask API..."

                python app.py > server.log 2>&1 &
                APP_PID=$!

                echo "Waiting for API to start..."
                sleep 10

                echo "Running tests..."
                pytest tests/

                echo "Stopping Flask server..."
                kill $APP_PID || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t employee-api .
                '''
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