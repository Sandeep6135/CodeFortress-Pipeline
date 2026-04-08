# CodeFortress CI – DevSecOps Pipeline

Automated Application Security Pipeline implementing Shift-Left Security across the entire SDLC.

## Overview

**CodeFortress CI** enforces security-first practices by detecting vulnerabilities, secrets, and misconfigurations before code reaches production. The pipeline automatically blocks insecure commits, runs comprehensive security scans (SAST/DAST), and aggregates findings in a centralized dashboard.

## Quick Start

1. **Setup**: Follow [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) to configure Jenkins, SonarQube, and DefectDojo
2. **Local Testing**: Run pre-commit TruffleHog hooks to detect secrets before push
3. **View Results**: Access DefectDojo dashboard after pipeline execution
4. **Reference**: See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system design

## Security Pipeline

```
Developer Commit
    ↓
Secret Detection (TruffleHog)
    ↓
CI Orchestration (Jenkins)
    ↓
SAST Analysis (SonarQube)
    ↓
Build & Stage (Docker)
    ↓
DAST Scanning (OWASP ZAP)
    ↓
Report Aggregation (DefectDojo)
    ↓
Approval Decision (PASS/FAIL)
```

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Secret Scanning | TruffleHog | Credential detection |
| SAST | SonarQube | Code vulnerability analysis |
| DAST | OWASP ZAP | Runtime security testing |
| CI/CD | Jenkins | Pipeline automation |
| Container | Docker | Environment standardization |
| Reporting | DefectDojo | Vulnerability aggregation |

## Key Features

- **Pre-commit Protection**: TruffleHog blocks commits with hardcoded secrets
- **Code Quality Gates**: SonarQube fails on critical vulnerabilities (SQLi, XSS, etc.)
- **Runtime Validation**: OWASP ZAP tests deployed application
- **Unified Dashboard**: DefectDojo provides single source of truth
- **Automated Enforcement**: No critical issues can bypass security gates

## Security Policy

- ✓ Zero critical vulnerabilities in production
- ✓ No hardcoded secrets allowed
- ✓ All merges require passing security gates
- ✓ All vulnerabilities logged and tracked

## Project Structure

```
CodeFortress-CI/
├── src/                    # Target Flask application
├── docker/                 # Container configurations
├── zap/                    # DAST scan profiles
├── scripts/                # Utility scripts
├── reports/                # Scan outputs
├── Jenkinsfile            # CI/CD pipeline definition
├── ARCHITECTURE.md        # System design details
├── DEPLOYMENT_GUIDE.md    # Setup instructions
├── TESTING.md             # Test procedures
└── README.md              # This file
```

## Documentation

- [Architecture](./ARCHITECTURE.md) – System design, data flow, and component interactions
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) – Setup, configuration, and troubleshooting
- [Testing](./TESTING.md) – Test scenarios and validation procedures

## Philosophy

**Security is not optional. It is enforced at every stage of development.**

Trust No One. Verify Everything.

## Author

Sandeep Hamirbhai Karmata – Cyber Security | DevSecOps