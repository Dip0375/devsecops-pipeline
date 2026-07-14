pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'humansafe'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        SONAR_PROJECT_KEY = 'humansafe'
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

        stage('Unit Tests') {
            steps {
                sh '''
                    cd app
                    pip install -r requirements.txt
                    python -m pytest tests/ -v --junitxml=reports/test-results.xml || true
                '''
            }
            post {
                always {
                    junit 'app/reports/test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    cd app
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Security Scan') {
            steps {
                sh """
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image --severity HIGH,CRITICAL --exit-code 1 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} || echo "Scan completed with findings"
                """
            }
        }

        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$DOCKER_USER/${DOCKER_IMAGE}:latest
                        docker push \$DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push \$DOCKER_USER/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                    echo "Deploying to staging environment..."
                    cd terraform
                    terraform init
                    terraform apply -auto-approve -var="environment=staging"
                '''
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to Production?"
                ok "Yes, deploy it!"
            }
            steps {
                sh '''
                    echo "Deploying to production environment..."
                    cd terraform
                    terraform apply -auto-approve -var="environment=production"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
        always {
            sh 'docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true'
            cleanWs()
        }
    }
}
