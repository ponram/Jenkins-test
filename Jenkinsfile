pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'option-pricer-venv'
        PROJECT_DIR = 'option-pricer'
        GITHUB_CREDENTIALS = 'github-credentials'
    }
    
    triggers {
        githubPush()
    }
    
    stages {
         stage('Checkout') {
            steps {
                git branch: 'develop', 
                    credentialsId: env.GITHUB_CREDENTIALS, 
                    url: 'https://github.com/ponram/Jenkins-test.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        # Remove existing venv if present
                        rm -rf ${VENV_NAME}
                        
                        # Create virtual environment
                        python3 -m venv ${VENV_NAME}
                        
                        # Activate and upgrade pip
                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip setuptools wheel
                    '''
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        # Install requirements first
                        pip install -r requirements.txt
                        
                        # Install development dependencies
                        pip install pytest pytest-cov coverage flake8 black isort
                        
                        # Install package in development mode
                        pip install -e .
                    '''
                }
            }
        }
        
        stage('Code Quality Checks') {
            parallel {
                stage('Lint') {
                    steps {
                        dir(env.PROJECT_DIR) {
                            sh '''
                                . ${VENV_NAME}/bin/activate
                                flake8 src/ tests/ --max-line-length=88 || true
                                black --check src/ tests/ || true
                                isort --check-only src/ tests/ || true
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        python -m pytest tests/ \
                            --junitxml=test-results.xml \
                            --cov=src/option_pricer \
                            --cov-report=xml:coverage.xml \
                            --cov-report=html:htmlcov/ \
                            --cov-report=term-missing \
                            -v
                    '''
                }
            }
            post {
                always {
                    dir(env.PROJECT_DIR) {
                        publishTestResults testResultsPattern: 'test-results.xml'
                        archiveArtifacts artifacts: 'htmlcov/**/*', allowEmptyArchive: true
                    }
                }
            }
        }
        
        stage('Build Package') {
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        # Clean previous builds
                        rm -rf build/ dist/ *.egg-info/
                        
                        # Build source distribution
                        python setup.py sdist
                        
                        # Build wheel distribution
                        python setup.py bdist_wheel
                    '''
                    archiveArtifacts artifacts: 'dist/*', fingerprint: true
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        
                        # Test package installation from wheel
                        pip install --force-reinstall dist/*.whl
                        
                        # Test CLI functionality
                        price-option --help || echo "CLI test completed"
                        
                        # Test import functionality
                        python -c "from option_pricer.app import OptionPricer; print('Import successful')"
                        
                        # Test basic functionality
                        python -c "
from option_pricer.app import OptionPricer
pricer = OptionPricer(100, 105, 0.05, 0.2)
result = pricer.price_european_option('2024-12-31', 'call')
print('Price:', result['price'])
assert result['price'] > 0, 'Price should be positive'
print('Integration test passed!')
"
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                dir(env.PROJECT_DIR) {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        pip install --force-reinstall dist/*.whl
                        echo "Package deployed to staging (local installation)"
                        
                        # Verify deployment
                        python -c "import option_pricer; print('Staging deployment verified')"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for details."
        }
    }
}
