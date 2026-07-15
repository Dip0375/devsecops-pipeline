pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_PROJECT_NAME = 'HumanSafe'
        SONAR_TOKEN = credentials('sonar-token')
        SONAR_URL = 'http://44.244.86.26:9000'
        DOCKER_IMAGE = 'infinite375/humansafe'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
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

        stage('Collect Sonar Metrics') {
            steps {
                sh """
                    curl -s -u ${SONAR_TOKEN}: \
                    "${SONAR_URL}/api/measures/component?component=${SONAR_PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,coverage,security_hotspots,duplicated_lines_density,reliability_rating,security_rating,sqale_rating" \
                    -o reports/sonar.json
                """
                script {
                    def sonar = readJSON file: 'reports/sonar.json'
                    def measures = [:]
                    sonar.component.measures.each { m ->
                        measures[m.metric] = m.value
                    }
                    env.SONAR_BUGS = measures.bugs ?: '0'
                    env.SONAR_VULNERABILITIES = measures.vulnerabilities ?: '0'
                    env.SONAR_CODE_SMELLS = measures.code_smells ?: '0'
                    env.SONAR_COVERAGE = measures.coverage ?: '0'
                    env.SONAR_SECURITY_HOTSPOTS = measures.security_hotspots ?: '0'
                    env.SONAR_DUPLICATION = measures.duplicated_lines_density ?: '0'
                }
            }
        }

        stage('Checkov Scan') {
            steps {
                script {
                    sh '''
                        checkov -d terraform/ -o json --output-file-path reports/checkov.json || true
                    '''

                    def checkov = readJSON file: 'reports/checkov.json'
                    def passed = checkov.summary?.passed ?: 0
                    def failed = checkov.summary?.failed ?: 0
                    def skipped = checkov.summary?.skipped ?: 0

                    env.CHECKOV_PASSED = "${passed}"
                    env.CHECKOV_FAILED = "${failed}"
                    env.CHECKOV_SKIPPED = "${skipped}"
                }
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                    trivy fs --format json --output reports/trivy-fs.json --severity HIGH,CRITICAL app/ || true
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
                }
            }
        }

        stage('Trivy Secret Scan') {
            steps {
                sh '''
                    trivy fs --scanners secret --format json --output reports/trivy-secret.json app/ || true
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
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} app/
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    trivy image --format json --output reports/trivy-image.json --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                '''
                script {
                    def trivyImage = readJSON file: 'reports/trivy-image.json'
                    def critical = 0
                    def high = 0

                    if (trivyImage.Results) {
                        trivyImage.Results.each { result ->
                            if (result.Vulnerabilities) {
                                result.Vulnerabilities.each { vuln ->
                                    if (vuln.Severity == 'CRITICAL') critical++
                                    if (vuln.Severity == 'HIGH') high++
                                }
                            }
                        }
                    }

                    env.TRIVY_IMAGE_CRITICAL = "${critical}"
                    env.TRIVY_IMAGE_HIGH = "${high}"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Generate HTML Report') {
            steps {
                script {
                    def qualityGateStatus = currentBuild.currentResult == 'SUCCESS' ? 'PASS' : 'UNSTABLE'
                    def report = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4; }
        .container { max-width: 700px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #1D3557, #457B9D); color: white; padding: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 28px; }
        .header p { margin: 5px 0 0; opacity: 0.9; }
        .status-bar { background: #27ae60; color: white; text-align: center; padding: 12px; font-size: 18px; font-weight: bold; }
        .status-bar.unstable { background: #f39c12; }
        .status-bar.failed { background: #e74c3c; }
        .section { padding: 20px 30px; border-bottom: 1px solid #eee; }
        .section:last-child { border-bottom: none; }
        .section h2 { color: #1D3557; font-size: 18px; margin: 0 0 15px; padding-bottom: 8px; border-bottom: 2px solid #E63946; display: inline-block; }
        .metrics { display: flex; flex-wrap: wrap; gap: 10px; }
        .metric { background: #f8f9fa; padding: 12px 16px; border-radius: 8px; flex: 1; min-width: 120px; text-align: center; }
        .metric .value { font-size: 24px; font-weight: bold; color: #1D3557; display: block; }
        .metric .label { font-size: 12px; color: #666; text-transform: uppercase; }
        .metric.pass { border-left: 4px solid #27ae60; }
        .metric.warn { border-left: 4px solid #f39c12; }
        .metric.fail { border-left: 4px solid #e74c3c; }
        .links { padding: 20px 30px; background: #f8f9fa; }
        .links a { display: inline-block; margin: 5px 10px 5px 0; color: #457B9D; text-decoration: none; font-weight: 500; }
        .links a:hover { text-decoration: underline; }
        .footer { text-align: center; padding: 15px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ HumanSafe - Security Report</h1>
            <p>Build #${env.BUILD_NUMBER} | Branch: ${env.GIT_BRANCH} | Commit: ${env.GIT_COMMIT_SHORT}</p>
        </div>

        <div class="status-bar ${env.BUILD_RESULT == 'SUCCESS' ? '' : 'unstable'}">
            ${env.BUILD_RESULT == 'SUCCESS' ? '✅ PIPELINE SUCCESS' : '⚠️ PIPELINE UNSTABLE - Security Issues Found'}
        </div>

        <div class="section">
            <h2>📊 SonarQube</h2>
            <div class="metrics">
                <div class="metric ${env.SONAR_BUGS?.toInteger() == 0 ? 'pass' : 'warn'}">
                    <span class="value">${env.SONAR_BUGS ?: '0'}</span>
                    <span class="label">Bugs</span>
                </div>
                <div class="metric ${env.SONAR_VULNERABILITIES?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.SONAR_VULNERABILITIES ?: '0'}</span>
                    <span class="label">Vulnerabilities</span>
                </div>
                <div class="metric pass">
                    <span class="value">${env.SONAR_CODE_SMELLS ?: '0'}</span>
                    <span class="label">Code Smells</span>
                </div>
                <div class="metric ${env.SONAR_COVERAGE?.toDouble() >= 80 ? 'pass' : 'warn'}">
                    <span class="value">${env.SONAR_COVERAGE ?: '0'}%</span>
                    <span class="label">Coverage</span>
                </div>
                <div class="metric pass">
                    <span class="value">${env.SONAR_SECURITY_HOTSPOTS ?: '0'}</span>
                    <span class="label">Security Hotspots</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔒 Checkov (Terraform)</h2>
            <div class="metrics">
                <div class="metric pass">
                    <span class="value">${env.CHECKOV_PASSED ?: '0'}</span>
                    <span class="label">Passed</span>
                </div>
                <div class="metric ${env.CHECKOV_FAILED?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.CHECKOV_FAILED ?: '0'}</span>
                    <span class="label">Failed</span>
                </div>
                <div class="metric pass">
                    <span class="value">${env.CHECKOV_SKIPPED ?: '0'}</span>
                    <span class="label">Skipped</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🐳 Trivy - Filesystem</h2>
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
            <h2>🔑 Trivy - Secrets</h2>
            <div class="metrics">
                <div class="metric ${env.TRIVY_SECRETS?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.TRIVY_SECRETS ?: '0'}</span>
                    <span class="label">Secrets Found</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>📦 Docker Image</h2>
            <div class="metrics">
                <div class="metric ${env.TRIVY_IMAGE_CRITICAL?.toInteger() == 0 ? 'pass' : 'fail'}">
                    <span class="value">${env.TRIVY_IMAGE_CRITICAL ?: '0'}</span>
                    <span class="label">Critical</span>
                </div>
                <div class="metric ${env.TRIVY_IMAGE_HIGH?.toInteger() == 0 ? 'pass' : 'warn'}">
                    <span class="value">${env.TRIVY_IMAGE_HIGH ?: '0'}</span>
                    <span class="label">High</span>
                </div>
                <div class="metric pass">
                    <span class="value">${DOCKER_IMAGE}:${DOCKER_TAG}</span>
                    <span class="label">Image</span>
                </div>
            </div>
        </div>

        <div class="links">
            <strong>🔗 Links:</strong><br>
            <a href="${env.BUILD_URL}">Jenkins Build</a>
            <a href="${SONAR_URL}/dashboard?id=${SONAR_PROJECT_KEY}">SonarQube Dashboard</a>
            <a href="https://hub.docker.com/r/${DOCKER_IMAGE}">Docker Hub</a>
        </div>

        <div class="footer">
            Generated by HumanSafe DevSecOps Pipeline | ${new Date().format('yyyy-MM-dd HH:mm:ss')}
        </div>
    </div>
</body>
</html>
"""
                    writeFile file: 'reports/security-report.html', text: report
                }
            }
        }

        stage('Send Email Report') {
            steps {
                emailext(
                    subject: "${currentBuild.currentResult == 'SUCCESS' ? '✅' : '⚠️'} DevSecOps Pipeline ${currentBuild.currentResult} | ${SONAR_PROJECT_NAME} | Build #${env.BUILD_NUMBER}",
                    body: '${FILE, path="reports/security-report.html"}',
                    to: "${RECIPIENT_EMAIL}",
                    mimeType: 'text/html',
                    attachLog: false
                )
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
