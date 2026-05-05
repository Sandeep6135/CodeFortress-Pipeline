<h1 align="center">CodeFortress</h1>

<p align="center">
  <b>Minimal, Usable DevSecOps Secret Scanner & Pipeline Orchestrator</b>
</p>

<p align="center">
  <a href="https://github.com/Sandeep6135/CodeFortress-Pipeline/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Sandeep6135/CodeFortress-Pipeline?style=flat-square" alt="License"></a>
</p>

## 🚀 Overview

**CodeFortress** is a lightweight security pipeline tool designed to catch hardcoded secrets before they are committed to version control. While many security tools are complex and require massive infrastructure, CodeFortress provides an immediate, runnable CLI tool to audit your codebase locally, alongside Docker deployment scripts for Jenkins CI integrations.

## ✨ Current Capabilities

- **Local Secret Scanning:** Run a Python-based CLI to detect hardcoded API keys, passwords, and private keys using regex patterns.
- **Dockerized CI Components:** A `deploy/docker-compose.yml` to spin up Jenkins, SonarQube, and DefectDojo locally.

## 🚧 Planned Features

- **SAST Integration:** Automating SonarQube scans via the CLI.
- **DAST Integration:** Spinning up ZAP proxies against local Docker containers.
- **Auto-Triaging:** Using LLMs to filter false positives from scan results.

## 🏗️ Project Structure

```text
CodeFortress-Pipeline/
├── cli/                      # CLI tool source code (secret scanner)
├── core/                     # Pipeline configurations (Jenkinsfiles)
├── deploy/                   # Docker-compose files for infrastructure setup
├── docs/                     # Extended documentation and architecture diagrams
├── examples/                 # Sample vulnerable targets for testing
├── tests/                    # Automated testing suite
├── main.py                   # Main CLI entry point
└── requirements.txt          # Python dependencies
```

## ⚙️ Installation

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repository
git clone https://github.com/Sandeep6135/CodeFortress-Pipeline.git
cd CodeFortress-Pipeline

# 2. Install dependencies
pip install -r requirements.txt
```

## 💻 Usage (CLI)

Run the CodeFortress CLI to scan any directory for secrets.

```bash
python main.py ./examples
```

## 📸 Proof of Execution

**Command:**
```bash
python main.py ./examples
```

**Expected Output (on the provided `vulnerable-app` example):**
```text
[+] Initializing CodeFortress Scanner...
[+] Target: ./examples

==================================================
[*] CodeFortress Security Report
==================================================
Status: [X] FAILED (1 issues detected)

1. [AWS Access Key] found in ./examples/vulnerable-app/app.py (Line 7)

[!] Please remove these secrets before committing.
```
*(If you run it on a clean directory, it will return `Status: [v] PASSED (0 secrets found)`).*

## 🐳 Usage (Docker Pipeline)

To stand up the Jenkins, SonarQube, and DefectDojo infrastructure:

```bash
cd deploy
docker-compose up -d
```

## 🤝 Contributing

Read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## 🛡️ Security

Please refer to our [Security Policy](SECURITY.md) for reporting vulnerabilities.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.