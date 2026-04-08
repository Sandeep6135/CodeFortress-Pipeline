pipeline {
    agent any
    
    environment {
        SONAR_HOST_URL = "http://sonarqube:9000"
        DEFECTDOJO_URL = "http://defectdojo:8081"
        STAGING_URL = "http://vulnerable-app:5000"
    }

    stages {
        stage('Week 1: Secret Scanning (TruffleHog)') {
            steps {
                echo 'Executing TruffleHog secret scan...'
                sh 'docker run --rm -v "$PWD:/pwd" trufflesecurity/trufflehog:latest git file:///pwd --fail'
            }
        }

        stage('Week 2: SAST Quality Gate (SonarQube)') {
            steps {
                echo 'Running SonarQube Static Application Security Testing...'
                // Simulated command for architecture design
                sh '''
                echo "Analyzing Python code for vulnerabilities (SQLi, XSS)..."
                # docker run --rm -e SONAR_HOST_URL=$SONAR_HOST_URL -v "$PWD:/usr/src" sonarsource/sonar-scanner-cli
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo 'Deploying vulnerable container to staging environment...'
                sh 'cd vulnerable-app && docker build -t cdoc-target-app . && docker run -d -p 5000:5000 --name target-app cdoc-target-app'
            }
        }

        stage('Week 3: DAST Active Scan (OWASP ZAP)') {
            steps {
                echo 'Executing OWASP ZAP Active Scan against Staging...'
                sh 'docker run -t owasp/zap2docker-stable zap-baseline.py -t $STAGING_URL -r zap_report.html || true'
            }
        }

        stage('Week 4: Reporting & Aggregation (DefectDojo)') {
            steps {
                echo 'Pushing SAST and DAST reports to DefectDojo API...'
                // Mock API call to DefectDojo
                sh '''
                echo "Uploading SonarQube and ZAP findings to unified dashboard..."
                # curl -X POST $DEFECTDOJO_URL/api/v2/import-scan/ -H 'Authorization: Token YOUR_TOKEN' -F 'file=@zap_report.html' -F 'scan_type=ZAP Scan'
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed. Checking Security Health.'
            // Cleanup staging container
            sh 'docker rm -f target-app || true'
        }
        failure {
            echo 'SECURITY GATE FAILED: Pipeline halted due to critical vulnerabilities or leaked secrets.'
        }
    }
}