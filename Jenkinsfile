pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_HOST = 'http://44.244.86.26:9000'
        REPORT_DIR = 'reports'
        DOCKER_IMAGE = 'infinite375/humansafe'
        IMAGE_TAG = "${BUILD_NUMBER}"
        RECIPIENT_EMAIL = "dipakpore375@gmail.com"
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:/usr/bin:/bin:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'mkdir -p reports'
                script {
                    env.GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
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
                        mkdir -p reports
                        curl -s -u "$SONAR_TOKEN:" \
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
                    env.SONAR_BUGS = measures.bugs ?: '0'
                    env.SONAR_VULNS = measures.vulnerabilities ?: '0'
                    env.SONAR_SMELLS = measures.code_smells ?: '0'
                    env.SONAR_COVERAGE = measures.coverage ?: '0'
                    env.SONAR_HOTSPOTS = measures.security_hotspots ?: '0'
                    echo "SonarQube: Bugs=${env.SONAR_BUGS}, Vulns=${env.SONAR_VULNS}, Smells=${env.SONAR_SMELLS}, Coverage=${env.SONAR_COVERAGE}%"
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
                    env.CHECKOV_PASSED = checkov.check_type?.sum { it.results?.passed?.size() ?: 0 } ?: 0
                    env.CHECKOV_FAILED = checkov.check_type?.sum { it.results?.failed?.size() ?: 0 } ?: 0
                    echo "Checkov: Passed=${env.CHECKOV_PASSED}, Failed=${env.CHECKOV_FAILED}"
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
                    env.TRIVY_FS_CRITICAL = "${critical}"
                    env.TRIVY_FS_HIGH = "${high}"
                    echo "Trivy FS: Critical=${critical}, High=${high}"
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
                    env.TRIVY_SECRETS = "${secretsFound}"
                    echo "Trivy Secrets: Found=${secretsFound}"
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

        stage('Generate HTML Report') {
            steps {
                script {
                    def report = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4; }
        .container { max-width: 700px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #1D3557, #457B9D); color: white; padding: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 26px; }
        .header p { margin: 5px 0 0; opacity: 0.9; font-size: 14px; }
        .section { padding: 20px 30px; border-bottom: 1px solid #eee; }
        .section h2 { color: #1D3557; font-size: 16px; margin: 0 0 12px; }
        .metrics { display: flex; flex-wrap: wrap; gap: 8px; }
        .metric { background: #f8f9fa; padding: 10px 14px; border-radius: 6px; flex: 1; min-width: 100px; text-align: center; }
        .metric .value { font-size: 20px; font-weight: bold; color: #1D3557; display: block; }
        .metric .label { font-size: 11px; color: #666; text-transform: uppercase; }
        .pass { border-left: 3px solid #27ae60; }
        .warn { border-left: 3px solid #f39c12; }
        .fail { border-left: 3px solid #e74c3c; }
        .footer { text-align: center; padding: 15px; color: #999; font-size: 11px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>HumanSafe Security Report</h1>
            <p>Build #${env.BUILD_NUMBER} | Branch: ${env.GIT_BRANCH} | Commit: ${env.GIT_COMMIT_SHORT}</p>
        </div>

        <div class="section">
            <h2>SonarQube</h2>
            <div class="metrics">
                <div class="metric ${env.SONAR_BUGS?.toInteger() == 0 ? 'pass' : 'warn'}">
                    <span class="value">${env.SONAR_BUGS ?: '0'}</span>
                    <span class="label">Bugs</span>
                </div>
                <div class="metric ${env.SONAR_VULNS?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.SONAR_VULNS ?: '0'}</span>
                    <span class="label">Vulnerabilities</span>
                </div>
                <div class="metric pass">
                    <span class="value">${env.SONAR_SMELLS ?: '0'}</span>
                    <span class="label">Code Smells</span>
                </div>
                <div class="metric ${env.SONAR_COVERAGE?.toDouble() >= 80 ? 'pass' : 'warn'}">
                    <span class="value">${env.SONAR_COVERAGE ?: '0'}%</span>
                    <span class="label">Coverage</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Checkov (Terraform)</h2>
            <div class="metrics">
                <div class="metric pass">
                    <span class="value">${env.CHECKOV_PASSED ?: '0'}</span>
                    <span class="label">Passed</span>
                </div>
                <div class="metric ${env.CHECKOV_FAILED?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.CHECKOV_FAILED ?: '0'}</span>
                    <span class="label">Failed</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Trivy - Filesystem</h2>
            <div class="metrics">
                <div class="metric ${env.TRIVY_FS_CRITICAL?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.TRIVY_FS_CRITICAL ?: '0'}</span>
                    <span class="label">Critical</span>
                </div>
                <div class="metric ${env.TRIVY_FS_HIGH?.toInteger() == 0 ? 'pass' : 'warn'}">
                    <span class="value">${env.TRIVY_FS_HIGH ?: '0'}</span>
                    <span class="label">High</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Trivy - Secrets</h2>
            <div class="metrics">
                <div class="metric ${env.TRIVY_SECRETS?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.TRIVY_SECRETS ?: '0'}</span>
                    <span class="label">Secrets Found</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Docker</h2>
            <div class="metrics">
                <div class="metric pass">
                    <span class="value">${DOCKER_IMAGE}:${IMAGE_TAG}</span>
                    <span class="label">Image</span>
                </div>
            </div>
        </div>

        <div class="footer">
            HumanSafe DevSecOps Pipeline | ${new Date().format('yyyy-MM-dd HH:mm:ss')}
        </div>
    </div>
</body>
</html>
"""
                    writeFile file: 'reports/security-report.html', text: report
                    echo "HTML report generated: reports/security-report.html"
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**/*', fingerprint: true, allowEmptyArchive: true
            }
        }

        stage('Send Email') {
            steps {
                emailext(
                    subject: "DevSecOps Pipeline | Build #${env.BUILD_NUMBER} | ${SONAR_PROJECT_NAME}",
                    body: '${FILE, path="reports/security-report.html"}',
                    to: "${RECIPIENT_EMAIL}",
                    mimeType: 'text/html'
                )
                echo "Email sent to ${RECIPIENT_EMAIL}"
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
