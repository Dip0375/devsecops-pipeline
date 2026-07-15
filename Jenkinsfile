pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_HOST = 'http://44.244.86.26:9000'
        REPORT_DIR = 'reports'
        DOCKER_IMAGE = 'infinite375/humansafe'
        IMAGE_TAG = "${BUILD_NUMBER}"
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:/usr/bin:/bin:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo "Repository checked out successfully."
            }
        }

        stage('Prepare Reports') {
            steps {
                sh 'mkdir -p reports'
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
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

        stage('Collect Sonar Metrics') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        curl -s -u $SONAR_TOKEN: \
                        "$SONAR_HOST/api/measures/component?component=$SONAR_PROJECT_KEY&metricKeys=bugs,vulnerabilities,code_smells,coverage,security_hotspots,duplicated_lines_density" \
                        -o reports/sonar.json
                    '''
                }
                script {
                    def sonar = readJSON file: 'reports/sonar.json'
                    def measures = [:]
                    sonar.component.measures.each { m ->
                        measures[m.metric] = m.value
                    }
                    echo "=== SonarQube Metrics ==="
                    echo "Bugs: ${measures.bugs ?: '0'}"
                    echo "Vulnerabilities: ${measures.vulnerabilities ?: '0'}"
                    echo "Code Smells: ${measures.code_smells ?: '0'}"
                    echo "Coverage: ${measures.coverage ?: '0'}%"
                    echo "Security Hotspots: ${measures.security_hotspots ?: '0'}"
                }
            }
        }

        stage('Checkov Scan') {
            steps {
                sh '''
                    /var/lib/jenkins/.local/bin/checkov \
                    -d terraform \
                    -o json \
                    --output-file-path reports/checkov.json
                '''
                script {
                    def checkov = readJSON file: 'reports/checkov.json/checkov_result.json'
                    def passed = checkov.check_type?.sum { it.results?.passed?.size() ?: 0 } ?: 0
                    def failed = checkov.check_type?.sum { it.results?.failed?.size() ?: 0 } ?: 0
                    echo "=== Checkov Results ==="
                    echo "Passed: ${passed}"
                    echo "Failed: ${failed}"

                    if (failed > 0) {
                        def userInput = input(
                            message: "Checkov found ${failed} failed checks. Continue to next stages?",
                            ok: 'Submit',
                            parameters: [
                                choice(
                                    name: 'CHECKOV_DECISION',
                                    choices: ['No - Abort Pipeline', 'Yes - Continue to Trivy & Deploy'],
                                    description: 'Choose an action for failed Checkov checks'
                                )
                            ]
                        )

                        if (userInput == 'No - Abort Pipeline') {
                            error("Pipeline aborted by user due to ${failed} Checkov failures.")
                        } else {
                            echo "User chose to continue despite ${failed} Checkov failures."
                        }
                    }
                }
            }
        }

        stage('Trivy Filesystem') {
            steps {
                sh '''
                    trivy fs \
                    --format json \
                    -o reports/trivy-fs.json \
                    --severity HIGH,CRITICAL \
                    app/
                '''
                script {
                    def trivyFs = readJSON file: 'reports/trivy-fs.json'
                    def critical = 0
                    def high = 0
                    if (trivyFs.Results) {
                        trivyFs.Results.each { result ->
                            if (result.Vulnerabilities) {
                                result.Vulnerabilities.each { vuln ->
                                    if (vuln.Severity == 'CRITICAL') critical++
                                    if (vuln.Severity == 'HIGH') high++
                                }
                            }
                        }
                    }
                    echo "=== Trivy Filesystem Results ==="
                    echo "Critical: ${critical}"
                    echo "High: ${high}"
                }
            }
        }

        stage('Trivy Secret') {
            steps {
                sh '''
                    trivy fs \
                    --scanners secret \
                    --format json \
                    -o reports/trivy-secret.json \
                    app/
                '''
                script {
                    def trivySecret = readJSON file: 'reports/trivy-secret.json'
                    def secretsFound = 0
                    if (trivySecret.Results) {
                        trivySecret.Results.each { result ->
                            if (result.Secrets) {
                                secretsFound += result.Secrets.size()
                            }
                        }
                    }
                    echo "=== Trivy Secret Results ==="
                    echo "Secrets Found: ${secretsFound}"
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                    -t $DOCKER_IMAGE:$IMAGE_TAG \
                    app/
                '''
                echo "Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully."
        }
        failure {
            echo "Pipeline failed. Check logs."
        }
        always {
            cleanWs()
        }
    }
}
