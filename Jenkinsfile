pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'humansafe'
        SONAR_PROJECT_NAME = 'HumanSafe'
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:/usr/bin:/bin:${env.PATH}"
        RECIPIENT_EMAIL = "dipakpore375@gmail.com"
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
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate abortPipeline: true
                        def status = qg.status
                        def projectKey = env.SONAR_PROJECT_KEY

                        emailext(
                            subject: "SonarQube Quality Gate: ${status} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                            body: """
                                <h2>SonarQube Quality Gate Report</h2>
                                <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                                <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                                <p><strong>Status:</strong> ${status}</p>
                                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                <p>View details: ${env.BUILD_URL}sonarQube/</p>
                            """,
                            to: "${RECIPIENT_EMAIL}",
                            mimeType: 'text/html'
                        )
                    }
                }
            }
        }

        stage('Checkov Scan') {
            steps {
                script {
                    def checkovOutput = sh(
                        script: 'checkov -d terraform/ --quiet --compact 2>&1 || true',
                        returnStdout: true
                    )

                    def passed = 0
                    def failed = 0
                    def skipped = 0

                    if (checkovOutput =~ /Passed checks:\s*(\d+)/) {
                        passed = (checkovOutput =~ /Passed checks:\s*(\d+)/)[0][1]
                    }
                    if (checkovOutput =~ /Failed checks:\s*(\d+)/) {
                        failed = (checkovOutput =~ /Failed checks:\s*(\d+)/)[0][1]
                    }
                    if (checkovOutput =~ /Skipped checks:\s*(\d+)/) {
                        skipped = (checkovOutput =~ /Skipped checks:\s*(\d+)/)[0][1]
                    }

                    def status = failed.toInteger() > 0 ? "FAILED" : "PASSED"
                    def statusEmoji = failed.toInteger() > 0 ? "FAILED" : "PASSED"

                    emailext(
                        subject: "Checkov Scan: ${status} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                            <h2>Checkov Security Scan Report</h2>
                            <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                            <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                            <p><strong>Status:</strong> ${status}</p>
                            <hr>
                            <p><strong>Passed Checks:</strong> ${passed}</p>
                            <p><strong>Failed Checks:</strong> ${failed}</p>
                            <p><strong>Skipped Checks:</strong> ${skipped}</p>
                            <hr>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p>View details: ${env.BUILD_URL}</p>
                        """,
                        to: "${RECIPIENT_EMAIL}",
                        mimeType: 'text/html'
                    )

                    if (failed.toInteger() > 0) {
                        echo "Checkov found ${failed} issues. Continuing pipeline..."
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                script {
                    def trivyOutput = sh(
                        script: 'trivy fs --severity HIGH,CRITICAL app/ 2>&1 || true',
                        returnStdout: true
                    )

                    def highCount = 0
                    def criticalCount = 0

                    if (trivyOutput =~ /High:\s*(\d+)/) {
                        highCount = (trivyOutput =~ /High:\s*(\d+)/)[0][1]
                    }
                    if (trivyOutput =~ /Critical:\s*(\d+)/) {
                        criticalCount = (trivyOutput =~ /Critical:\s*(\d+)/)[0][1]
                    }

                    def totalVulns = highCount.toInteger() + criticalCount.toInteger()
                    def status = totalVulns > 0 ? "VULNERABILITIES FOUND" : "CLEAN"

                    emailext(
                        subject: "Trivy Filesystem Scan: ${status} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                            <h2>Trivy Filesystem Scan Report</h2>
                            <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                            <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                            <p><strong>Status:</strong> ${status}</p>
                            <hr>
                            <p><strong>High Severity:</strong> ${highCount}</p>
                            <p><strong>Critical Severity:</strong> ${criticalCount}</p>
                            <p><strong>Total Issues:</strong> ${totalVulns}</p>
                            <hr>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p>View details: ${env.BUILD_URL}</p>
                        """,
                        to: "${RECIPIENT_EMAIL}",
                        mimeType: 'text/html'
                    )

                    echo "Trivy Filesystem Scan completed."
                }
            }
        }

        stage('Trivy Secret Scan') {
            steps {
                script {
                    def secretOutput = sh(
                        script: 'trivy fs --scanners secret app/ 2>&1 || true',
                        returnStdout: true
                    )

                    def secretCount = 0
                    if (secretOutput =~ /Total number of secrets found:\s*(\d+)/) {
                        secretCount = (secretOutput =~ /Total number of secrets found:\s*(\d+)/)[0][1]
                    }

                    def status = secretCount.toInteger() > 0 ? "SECRETS FOUND" : "CLEAN"

                    emailext(
                        subject: "Trivy Secret Scan: ${status} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                            <h2>Trivy Secret Scan Report</h2>
                            <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                            <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                            <p><strong>Status:</strong> ${status}</p>
                            <hr>
                            <p><strong>Secrets Found:</strong> ${secretCount}</p>
                            <hr>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p>View details: ${env.BUILD_URL}</p>
                        """,
                        to: "${RECIPIENT_EMAIL}",
                        mimeType: 'text/html'
                    )

                    echo "Trivy Secret Scan completed."
                }
            }
        }
    }

    post {

        success {
            emailext(
                subject: "Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Pipeline Completed Successfully</h2>
                    <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                    <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> SUCCESS</p>
                    <p>All stages completed without failures.</p>
                    <p>View build: ${env.BUILD_URL}</p>
                """,
                to: "${RECIPIENT_EMAIL}",
                mimeType: 'text/html'
            )
        }

        failure {
            emailext(
                subject: "Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Pipeline Failed</h2>
                    <p><strong>Project:</strong> ${SONAR_PROJECT_NAME}</p>
                    <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> FAILED</p>
                    <p>Please check the console output for details.</p>
                    <p>View build: ${env.BUILD_URL}</p>
                """,
                to: "${RECIPIENT_EMAIL}",
                mimeType: 'text/html'
            )
        }

        always {
            cleanWs()
        }
    }
}
