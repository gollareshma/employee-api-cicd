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
        sh '''
        echo "Loading environment variables..."

        export DB_HOST=$DB_HOST
        export DB_USER=$DB_USER
        export DB_PASSWORD=$DB_PASSWORD
        export DB_NAME=$DB_NAME
        export JWT_SECRET=$JWT_SECRET
        export FLASK_ENV=production

        echo "Starting Flask API..."

        . venv/bin/activate
        python app.py &
        API_PID=$!

        echo "Flask PID: $API_PID"

        echo "Waiting for API..."
        sleep 8

        echo "Running tests..."
        pytest tests/ -v

        echo "Stopping API..."
        kill $API_PID
        '''
    }
}