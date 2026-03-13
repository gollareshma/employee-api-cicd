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

                # Start Flask app in background
                python app.py &
                APP_PID=$!

                # Wait for server to start
                sleep 5

                # Run tests
                pytest tests/

                # Stop the Flask server
                kill $APP_PID
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