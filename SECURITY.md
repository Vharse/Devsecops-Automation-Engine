# Security Policy

## Supported Versions

We actively maintain and apply security updates to the default primary branch (`main`). All reusable workflows and policies referenced from `main` are considered supported.

| Version / Branch | Supported          |
| ---------------- | ------------------ |
| `main`           | :white_check_mark: |
| `dev`            | :construction:     |
| `< v1.0.0`       | :x:                |

---

## Security Commitments & Architecture

The **DevSecOps Automation Engine** enforces zero-trust security controls across software delivery pipelines:

* **Static Analysis & Secret Detection**: All commits are analyzed via Gitleaks and Semgrep to prevent hardcoded credentials or unsafe patterns from reaching remote tracking branches.
* **Supply Chain Verification**: Third-party actions and container base images are pinned and scanned using Trivy and SPDX SBOM generation.
* **Governance**: OpenSSF Scorecard evaluations enforce supply chain and branch protection standards on primary releases.

---

## Reporting a Vulnerability

If you discover a security vulnerability, flaw, or credential leakage risk within this engine or its reusable workflows, please report it directly rather than opening a public issue.

### Disclosure Process

1. **Private Contact**: Send an email detailing the vulnerability to **vharse.security@gmail.com**.
2. **Details to Include**:
   * Type of issue (e.g., credential exposure, OPA policy bypass, malicious workflow injection).
   * Step-by-step proof-of-concept (PoC) or workflow trace demonstrating the risk.
   * Affected file(s) or line numbers (e.g., `.github/workflows/security-engine.yml`).
3. **Response Timeline**:
   * **Initial Acknowledgment**: Within 24–48 hours.
   * **Remediation & Patching**: Critical findings will be patched on `dev` and merged to `main` within 7 days.

---

## Security Best Practices for Consumers

When calling `security-engine.yml` in client repositories:

* Always pin workflow references to specific release tags or immutable commit SHAs rather than mutable branch names in production pipelines (e.g., `uses: onlyonelogix/Devsecops-Automation-Engine/.github/workflows/security-engine.yml@<COMMIT_SHA>`).
* Grant minimum necessary `permissions:` block scopes in caller workflows (Principle of Least Privilege).
* Restrict access to Elastic SIEM API keys and Slack webhook secrets stored within repository secrets.