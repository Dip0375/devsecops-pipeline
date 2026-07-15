pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_PROJECT_NAME = 'HumanSafe'
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:/usr/bin:/bin:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo "Repository checked out successfully."
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                              -Dsonar.projectName=${SONAR_PROJECT_NAME} \
                              -Dsonar.sources=app \
                              -Dsonar.python.version=3.11
                        """
                    }
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
                sh '''
                    echo "Running Checkov..."
                    checkov -d terraform/
                '''
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                    echo "Running Trivy Filesystem Scan..."
                    trivy fs --severity HIGH,CRITICAL app/
                '''
            }
        }

        stage('Trivy Secret Scan') {
            steps {
                sh '''
                    echo "Running Trivy Secret Scan..."
                    trivy fs --scanners secret app/
                '''
            }
        }
    }

    post {

        success {
            echo "DevSecOps Pipeline completed successfully."
        }

        failure {
            echo "Pipeline failed. Please review the console output."
        }

        always {
            cleanWs()
        }
    }
}
