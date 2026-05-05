import os
import re

# Simple regex patterns for common secrets
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API Key": r"api[_-]?key[\s=:\"']+([a-zA-Z0-9_\-]{20,})",
    "Password field": r"password[\s=:\"']+([a-zA-Z0-9_\-@!#$]{8,})",
    "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----"
}

def scan_file(file_path):
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                for secret_type, pattern in SECRET_PATTERNS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            "type": secret_type,
                            "line": line_num,
                            "file": file_path
                        })
    except Exception as e:
        pass # Ignore unreadable files for now
    return findings

def scan_directory(directory_path):
    all_findings = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            # Skip hidden folders like .git
            if '.git' in root:
                continue
            file_path = os.path.join(root, file)
            all_findings.extend(scan_file(file_path))
    return all_findings
