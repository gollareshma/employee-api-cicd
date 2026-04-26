pipeline {
    agent any

    stages {

        stage('Checkout Code') {
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

        stage('Start API & Run Tests') {
            steps {
                sh '''
                . venv/bin/activate

                echo "Starting Flask API..."
                nohup python app.py > server.log 2>&1 &
                APP_PID=$!

                echo "Waiting for API..."
                sleep 5

                echo "Running tests..."
                pytest tests/ -v

                echo "Stopping API..."
                kill $APP_PID || true
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS ✅'
        }
        failure {
            echo 'Pipeline FAILED ❌'
        }
    }
}