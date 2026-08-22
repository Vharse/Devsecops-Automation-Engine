## DevSecOps Automation Engine

An enterprise-grade, centralized DevSecOps Automation Engine designed to standardize security gates across modern CI/CD software delivery pipelines. Built with modular, reusable workflows, this engine automatically enforces Static Application Security Testing (SAST), Code Quality analysis, Secret Scanning, Software Bill of Materials (SBOM) generation, Infrastructure-as-Code (IaC) policy compliance, OpenSSF supply chain security posture checks, and real-time SIEM event correlation.

## 🏛️ Architecture Overview

The DevSecOps Automation Engine functions as a centralized security authority. Client repositories or local pipelines call reusable workflows to enforce shift-left security before code compilation or deployment.

                                      ┌─────────────────────────────────────────┐
                                      │          Developer Push / PR            │
                                      └────────────────────┬────────────────────┘
                                                          │
                                                          ▼
                                      ┌─────────────────────────────────────────┐
                                      │    GitHub Actions Security Workflow     │
                                      └────────────────────┬────────────────────┘
                                                        │
                ┌────────────────────────────┼────────────────────────────┬────────────────────────────┐
                │                            │                            │                            │
                ▼                            ▼                            ▼                            ▼
      ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
      │ SAST, Quality &  │         │ Container & SBOM │         │ IaC Policy Guard │         │ OpenSSF Posture  │
      │ Secret Scanning  │         │ Scanning         │         │ (OPA / Rego)     │         │ Evaluation       │
      ├──────────────────┤         ├──────────────────┤         ├──────────────────┤         ├──────────────────┤
      │ • Gitleaks       │         │ • Trivy Scanner  │         │ • OPA Rego Engine│         │ • Scorecard v2   │
      │ • Semgrep Rules  │         │ • SPDX SBOM      │         │ • S3/IaC Checks  │         │ • SARIF Export   │
      │ • SonarQube Gate │         └────────┬─────────┘         └────────┬─────────┘         └────────┬─────────┘
      └────────┬─────────┘                  │                            │                            │
              │                            │                            │                            │
              └────────────────────────────┴─────────────┬──────────────┴────────────────────────────┘
                                                          │
                                                          ▼
                                      ┌─────────────────────────────────────────┐
                                      │    Elastic SIEM Telemetry Collector     │
                                      │       (devsecops-pipeline-logs)         │
                                      └─────────────────────────────────────────┘
                                                          │
                                                          ▼
                                      ┌─────────────────────────────────────────┐
                                      │       Slack Automated Incident          │
                                      │           Alert Dispatcher              │
                                      └─────────────────────────────────────────┘
```


```
🚀 Key Accomplishments & Technical Features
1. Reusable Workflow Security Gate (devsecops-gate.yml)

    Implemented modular GitHub Actions workflow (.github/workflows/security-engine.yml) that can be centrally referenced across organizational repositories.

    Enforces strict quality and security gates prior to code merge or release.

2. Static Code, Quality & Secret Analysis (SAST)

    Secret Detection: Integrated Gitleaks to detect hardcoded high-entropy strings, API keys, passwords, and private SSH keys across all git commits.

    Semgrep SAST: Linked Semgrep AppSec Platform for automated SAST scanning to uncover code vulnerabilities, injection threats, and unsafe coding practices.

    SonarQube Code Quality & SAST Gate: Integrated SonarQube static analysis for deep polyglot source code scanning, evaluating code smells, security hotspots, technical debt, and Quality Gate policies. Evaluates execution conditions dynamically using env context mapping to guarantee safe token parsing.

3. Container Security & Software Bill of Materials (SBOM)

    Trivy Vulnerability Scanner: Configured image scanning against application Dockerfile and base dependencies.

    SPDX SBOM Generation: Automated creation and artifact upload of standard SPDX SBOM reports to maintain software supply chain transparency.

4. Policy as Code Governance (OPA / Rego)

    Built custom Open Policy Agent rules (policies/opa/s3_check.rego) to validate Infrastructure-as-Code setups.

    Prevents misconfigurations (e.g., publicly accessible storage, weak encryption policies) from reaching deployment environments.

5. Supply Chain Security Posture (OpenSSF Scorecard)

    Integrated OpenSSF Scorecard to automatically evaluate repository security posture, branch protections, and supply chain health.

    Enforces automated default-branch guards (if: github.ref == 'refs/heads/main') to align with OpenSSF API policies while keeping developer feature branches (dev) fast and unblocked.

    Exports security posture metrics in SARIF format for centralized reporting.

6. Elastic SIEM Telemetry & Security Operations

    Formatted pipeline security events into JSON telemetry payloads.

    Integrated automated ingestion into Elasticsearch / Elastic SIEM (devsecops-pipeline-logs-* index) for real-time monitoring and SOC alert correlation across all scanning gates.

7. Automated Slack Incident Notifications

    Integrated Slack Incoming Webhooks via slackapi/slack-github-action for real-time alerting on pipeline execution outcomes.

    Dispatches formatted security status alerts (PASSED or FAILED), pipeline triggers, and actor metadata directly to designated security channels upon pipeline completion.


## 📂 Repository Structure

Devsecops-Automation-Engine/
├── .github/
│   └── workflows/
│       ├── clear-actions.yml      # Workflow run cleanup automation
│       ├── security-engine.yml    # Reusable core pipeline engine
│       └── security-check.yml     # Local execution pipeline
├── policies/
│   └── opa/
│       └── s3_check.rego          # OPA Rego compliance policies
├── src/
│   └── Dockerfile                 # Zero-CVE Chainguard container base
├── LICENSE                        # MIT Open Source License
├── README.md                      # System documentation
└── SECURITY.md                    # Vulnerability disclosure and security policy
---

## 🔑 Required Repository Secrets

To run all pipeline jobs successfully, configure these secrets under **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | Description | Example / Scope |
| :--- | :--- | :--- |
| `SEMGREP_APP_TOKEN` | Authentication token from Semgrep AppSec | `semgrep_...` |
| `SONAR_TOKEN	Global analysis authentication token for SonarQube	sqa_...` |
| `ELASTIC_HOST` | Endpoint URL for Elastic SIEM cluster | `https://elastic.your-domain.com:9243` |
| `ELASTIC_API_KEY` | Base64 encoded Elastic API Key for log ingestion | `V2...==` |
| `SLACK_WEBHOOK_URL` | *(Optional)* Slack Incoming Webhook URL for automated channel alerting | `https://hooks.slack.com/services/...` |

---

## 🛠️ Usage & Integration

### Reusing this Engine in Client Repositories

To consume this centralized security engine inside any client repository, create `.github/workflows/security-check.yml` in your target repo:

```yaml
name: Security Check

on:
  push:
    branches: [ "main", "dev" ]
  pull_request:
    branches: [ "main", "dev" ]

jobs:
  run-security-engine:
    uses: Vherse/Devsecops-Automation-Engine/.github/workflows/security-engine.yml@main
    permissions:
      contents: read
      security-events: write
      id-token: write
    secrets: inherit
      
```

---

## 📜 License

This project is open-source and distributed under the [MIT License](LICENSE).
