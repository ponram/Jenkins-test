// Jenkinsfile
pipeline {
    agent any // Tells Jenkins to run the pipeline on any available agent

    stages {
        stage('Checkout') {
            steps {
                // Automatically checks out the code from the SCM (Source Code Management)
                // defined in the Jenkins job configuration.
                git branch: 'main', url: 'https://github.com/ponram/Jenkins-test.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application...'
                // In a real Python project, "build" might involve:
                // - Installing dependencies: pip install -r requirements.txt
                // - Linting/Static analysis: pylint app.py
                // For this simple example, we'll just check Python syntax.
                sh 'python -m py_compile app.py'
                echo 'Build complete.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Execute the unit tests
                sh 'python -m unittest test_app.py'
                echo 'Tests complete.'
            }
        }

        stage('Deliver/Deploy') {
            steps {
                echo 'Simulating deployment...'
                // In a real-world scenario, this stage would involve:
                // - Building a Docker image
                // - Pushing to a container registry
                // - Deploying to a server (e.g., Kubernetes, AWS, Azure, GCP)
                // For this tutorial, we'll just print a message.
                sh 'echo "Application successfully built, tested, and ready for deployment!"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
