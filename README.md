# Project 1: DevSecOps - Automated Application Security Pipeline
**Product Brand Name:** CodeFortress CI/CD  
**Domain:** AppSec (Shift Left)

## Overview
This repository contains the infrastructure and pipeline logic to implement a robust CI/CD pipeline that automatically breaks the build if security thresholds are not met. The security integrations are fully automated to accelerate DevOps velocity while maintaining a "Zero Critical CVEs" quality gate.

## Tool Stack
* **TruffleHog:** High-speed secret scanning to detect leaked AWS keys and tokens.
* **SonarQube (SAST):** Static analysis for common security bugs (e.g., SQL Injection) prior to deployment.
* **OWASP ZAP (DAST):** Active dynamic scanning against running web applications in staging environments.
* **DefectDojo:** Unified vulnerability reporting and aggregation dashboard.

## Pipeline Architecture
1. **Pre-commit:** Local developers run TruffleHog hooks to prevent secrets from entering the remote repo.
2. **Commit:** Jenkins triggers the `Jenkinsfile` pipeline.
3. **Scan:** SonarQube analyzes the source code against strict Quality Profiles.
4. **Deploy & Attack:** Application is containerized to Staging, where OWASP ZAP spiders and attacks the runtime environment.
5. **Report:** All findings are pushed to DefectDojo via API for a final Executive Security Health report.
