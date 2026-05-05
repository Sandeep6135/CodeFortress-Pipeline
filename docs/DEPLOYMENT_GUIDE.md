# CodeFortress CI/CD - Deployment & Setup Guide

**Target Audience:** DevOps Engineers, Security Engineers  
**Estimated Setup Time:** 30-45 minutes  
**Prerequisites:** Docker, Docker Compose, Git, Jenkins (optional: local Jenkins)

---

## Quick Start (5 minutes)

```bash
# Clone and navigate to project
cd CodeFortress-Pipeline

# Start all services
docker-compose up -d

# Verify services are healthy
docker-compose ps

# Access dashboards
echo "Jenkins: http://localhost:8080"
echo "SonarQube: http://localhost:9000"
echo "DefectDojo: http://localhost:8081"
```

---

## Step-by-Step Deployment

### 1. Prerequisites Verification

```bash
# Verify Docker is installed and running
docker --version  # Should be 20.10+
docker run hello-world

# Verify Docker Compose
docker-compose --version  # Should be 2.0+

# Verify Git
git --version

# Required disk space: ~15GB
# Required RAM: 8GB minimum (4GB for Jenkins, 2GB for SonarQube, 2GB for DefectDojo)
```

### 2. Deploy Infrastructure with Docker Compose

```bash
# Navigate to project directory
cd CodeFortress-Pipeline

# Create volumes directory
mkdir -p ./volumes/jenkins_data ./volumes/sonarqube_data

# Start all services
docker-compose up -d

# Monitor startup (may take 2-3 minutes)
docker-compose logs -f

# Once ready, you'll see similar output:
# jenkins    | Jenkins is fully up and running
# sonarqube  | SonarQube is ready
# defectdojo | DefectDojo Started Successfully
```

### 3. Configure Jenkins

#### 3.1 Initial Jenkins Access

```bash
# Retrieve initial admin password
docker-compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Navigate to http://localhost:8080
# Paste the password when prompted
```

#### 3.2 Install Required Jenkins Plugins

1. **Manage Jenkins** → **Plugin Manager**
2. **Available** tab → Search and install:
   - `TruffleHog` (or `TruffleHog Scan`)
   - `SonarQube Scanner`
   - `Docker` plugin
   - `Email Extension`
   - `Generic Webhook Trigger`

#### 3.3 Create Pipeline Job

```bash
# Via Jenkins UI:
1. Click "New Item"
2. Name: "CodeFortress-Security-Pipeline"
3. Type: "Pipeline"
4. In "Pipeline" section:
   - Definition: "Pipeline script from SCM"
   - SCM: "Git"
   - Repository URL: <your-git-repo-url>
   - Branch: "main"
   - Script Path: "Jenkinsfile"
5. Save & Build Now
```

### 4. Install Pre-Commit Hooks (Developer Machines)

```bash
# For each developer workstation
cd your-application-repo

# Install pre-commit framework
pip install pre-commit

# Copy or symlink pre-commit config
cp CodeFortress-Pipeline/.pre-commit-config.yaml .

# Install hooks
pre-commit install

# Test the hook
# Attempting to commit an AWS key should fail automatically
echo "AKIAIOSFODNN7EXAMPLE" >> test.txt
git add test.txt
git commit -m "test" # This will fail - TruffleHog will block it
```

### 5. Configure SonarQube

#### 5.1 SonarQube Initial Setup

```bash
# Navigate to http://localhost:9000
# Default credentials: admin / admin
# Change password when prompted

# Create new project:
# 1. Click "Create project" or Projects → Create Project
# 2. Project key: "CodeFortress"
# 3. Display name: "CodeFortress Security Pipeline"
```

#### 5.2 Generate SonarQube Token

```bash
# In SonarQube UI:
# 1. Go to "Administration" → "Security" → "Tokens"
# 2. Click "Generate Tokens"
# 3. Name: "Jenkins-Token"
# 4. Select scopes: analyze
# 5. Copy token
# 6. In Jenkins: Add to Credentials (Jenkins → Manage Credentials)
```

#### 5.3 Configure Quality Gate

```bash
# In SonarQube:
# 1. Quality Gates → Create
# 2. Name: "Zero Critical CVEs"
# 3. Add conditions:
#    - Metric: "Critical Issues" | Operator: ">" | Error: 0
#    - Metric: "High Issues" | Operator: ">" | Error: 0 (in auth code)
# 4. Save and set as default
```

### 6. Setup DefectDojo

#### 6.1 Initial Access

```bash
# Navigate to http://localhost:8081
# Credentials generated from environment (see docker-compose.yml)
```

#### 6.2 Create DefectDojo Token

```bash
# In DefectDojo UI:
# 1. User Profile → API Keys
# 2. Click "Generate API Key"
# 3. Copy token
# 4. Add to Jenkins Credentials
```

#### 6.3 Create DefectDojo Product

```bash
# In DefectDojo UI:
# 1. Products → Add Product
# 2. Name: "CodeFortress"
# 3. Product Type: "Generic"
# 4. Save
```

### 7. Test the Pipeline

#### 7.1 Trigger Secret Scanning (Week 1 Gate Check)

```bash
# Create a test commit with a fake secret
echo "AWS_SECRET_ACCESS_KEY='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'" > test.py

# Attempt to commit (pre-commit hook should catch it)
git add test.py
git commit -m "test"

# Expected: ✗ FAIL - TruffleHog detected secret
```

#### 7.2 Trigger SAST Scanning (Week 2 Gate Check)

```bash
# In Jenkins:
# 1. Trigger build manually
# 2. Watch pipeline execution
# 3. Check SonarQube dashboard for findings
# 4. Verify pipeline fails if High/Critical issues detected
```

#### 7.3 Trigger DAST Scanning (Week 3 Gate Check)

```bash
# Pipeline will:
# 1. Build vulnerable-app Docker image
# 2. Run container on port 5000
# 3. Execute OWASP ZAP against http://vulnerable-app:5000
# 4. Generate report

# Check ZAP reports in Jenkins workspace for:
# - SQL Injection findings (vulnerable /user endpoint)
# - Other web vulnerabilities
```

#### 7.4 Verify DefectDojo Integration (Week 4 Gate Check)

```bash
# After pipeline completes:
# 1. Check DefectDojo dashboard
# 2. Verify findings are aggregated from all scanners
# 3. Confirm you can filter by severity, tool, etc.
```

### 8. Configure Notifications

#### 8.1 Email Notifications

```bash
# In Jenkins: Manage Jenkins → Configure System
# Set up email notifications:
# - SMTP Server: (your organization's SMTP)
# - Default user email: security-team@company.com
# - Enable TLS/SSL if required
```

#### 8.2 Slack Notifications (Optional)

```bash
# In Jenkins:
# 1. Install "Slack" plugin
# 2. Configure Slack integration in Jenkinsfile
# 3. On security gate failure, Slack messages will be sent

# Example Jenkinsfile snippet:
# post {
#     failure {
#         slackSend(channel: '#security', message: 'CodeFortress Pipeline FAILED')
#     }
# }
```

---

## Operational Procedures

### Running a Complete Pipeline

```bash
# Option 1: Via Jenkins UI
# 1. Navigateto Jenkins Dashboard
# 2. Click "CodeFortress-Security-Pipeline"
# 3. Click "Build Now"
# 4. Monitor build progress

# Option 2: Via Git webhook (automatic)
# Trigger: git push to main branch
# Jenkins automatically triggers pipeline

# Expected Runtime: ~8-12 minutes
# - Secret Scan: 30 seconds
# - SAST: 2-3 minutes
# - Docker build/deploy: 2 minutes
# - DAST: 3-4 minutes
# - Aggregation: 1 minute
```

### Viewing Reports

**TruffleHog Results:**
```bash
docker-compose exec jenkins cat /var/jenkins_home/workspace/CodeFortress-Security-Pipeline/truffelhog_report.json
```

**SonarQube Dashboard:**
```
http://localhost:9000 → Projects → CodeFortress
```

**ZAP Report:**
```bash
# Located in Jenkins workspace
/var/jenkins_home/workspace/CodeFortress-Security-Pipeline/zap_report.html
```

**DefectDojo Unified Dashboard:**
```
http://localhost:8081 → Products → CodeFortress → Engagements
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Jenkins won't start | Check port 8080 not in use: `lsof -i :8080` |
| SonarQube OOMKilled | Increase Docker memory: `edit docker-compose.yml environment.SONAR_JAVA_OPTS` |
| TruffleHog false positives | Configure ignore file: `.trufflehogscan.json` |
| ZAP timeout | Increase timeout in Jenkinsfile or reduce site complexity |
| DefectDojo API errors | Verify API token format and permissions |

### Backup & Recovery

```bash
# Backup Jenkins configuration
docker-compose exec jenkins tar -czf jenkins_backup.tar.gz /var/jenkins_home

# Backup SonarQube database
docker-compose exec sonarqube pg_dump sonar > sonarqube_backup.sql

# Restore
docker-compose exec jenkins tar -xzf jenkins_backup.tar.gz -C /
```

---

## Production Deployment Checklist

- [ ] Jenkins configured with persistent storage
- [ ] SonarQube connected to production database (not H2)
- [ ] DefectDojo database backed by PostgreSQL
- [ ] HTTPS/TLS enabled on all endpoints
- [ ] Sensitive credentials stored in Jenkins Credentials Vault
- [ ] Pre-commit hooks deployed to all developer machines
- [ ] Quality gates enforced in pipeline
- [ ] Notifications configured for security team
- [ ] Backup strategy implemented for all data
- [ ] Monitoring/alerting configured for pipeline failures

---

## Performance Tuning

```bash
# Increase Jenkins heap size for large codebases
docker-compose.yml environment section:
  JAVA_OPTS: "-Xmx4g"

# Increase SonarQube performance
environment:
  SONAR_JAVA_OPTS: "-Xmx2g"

# Parallel DAST scanning (advanced)
# Requires ZAP Pro license for optimization
```

---

## Security Hardening

✅ **Always:**
- Keep secrets out of docker-compose.yml (use Docker secrets or vault)
- Enable Jenkins authorization and  auditlogging
- Use strong passwords for all services
- Run services on non-standard ports
- Restrict network access to localhost during testing

❌ **Never:**
- Expose Jenkins/SonarQube to public internet without authentication
- Use default credentials
- Store API tokens in code
- Run containers as root unnecessarily

---

*Deployment is complete when all gate checks pass successfully.* ✅
