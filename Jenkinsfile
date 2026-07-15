pipeline {
    agent any

    tools {
        sonarQube 'SonarScanner'
    }

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_PROJECT_NAME = 'HumanSafe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                          -Dsonar.projectName=${SONAR_PROJECT_NAME} \
                          -Dsonar.sources=app \
                          -Dsonar.python.version=3.11
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Checkov Scan') {
            steps {
                sh 'checkov -d terraform/ --output cli --quiet'
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh 'trivy fs --severity HIGH,CRITICAL --exit-code 1 app/'
            }
        }

        stage('Trivy Secret Scan') {
            steps {
                sh 'trivy fs --scanners secret --severity HIGH,CRITICAL --exit-code 1 app/'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
