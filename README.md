DevSecOps Automation Engine

An enterprise-grade, centralized DevSecOps Automation Engine designed to standardize security gates across modern CI/CD software delivery pipelines. Built with modular, decoupled reusable workflows, this engine automatically enforces Static Application Security Testing (SAST), Code Quality analysis, independent Secret Scanning, Software Bill of Materials (SBOM) generation, Infrastructure-as-Code (IaC) policy compliance, OpenSSF supply chain security posture checks, centralized vulnerability management in DefectDojo, and real-time SIEM event correlation.
🏛️ Architecture Overview

The DevSecOps Automation Engine functions as a centralized security authority. Client repositories or local pipelines execute modular, parallel reusable workflows to enforce shift-left security before code compilation or deployment.
Plaintext

                                        ┌─────────────────────────────────────────┐
                                        │         Developer Push / PR             │
                                        └────────────────────┬────────────────────┘
                                                             │
                                                             ▼
                                        ┌─────────────────────────────────────────┐
                                        │    GitHub Actions Security Workflow     │
                                        └────────────────────┬────────────────────┘
                                                             │
        ┌────────────────────────────┬───────────────────────┴──────┬────────────────────────────┬────────────────────────────┐
        │                            │                              │                            │                            │
        ▼                            ▼                              ▼                            ▼                            ▼
  ┌───────────┐                ┌───────────┐                  ┌───────────┐                ┌───────────┐                ┌───────────┐
  │ SAST Scan │                │  Secret   │                  │ Container │                │    IaC    │                │  OpenSSF  │
  │  & Code   │                │ Scanning  │                  │  & SBOM   │                │  Policy   │                │  Posture  │
  │  Quality  │                │           │                  │ Scanning  │                │   Guard   │                │   Audit   │
  ├───────────┤                ├───────────┤                  ├───────────┤                ├───────────┤                ├───────────┤
  │ Semgrep   │                │ Gitleaks  │                  │ Trivy     │                │ OPA Rego  │                │ Scorecard │
  │ SonarQube │                │ Gate      │                  │ SPDX SBOM │                │ Engine    │                │ SARIF     │
  └─────┬─────┘                └─────┬─────┘                  └─────┬─────┘                └─────┬─────┘                └─────┬─────┘
        │                            │                              │                            │                            │
        └────────────────────────────┴──────────────┬───────────────┴────────────────────────────┴────────────────────────────┘
                                                    │
                                                    ▼
                                        ┌─────────────────────────────────────────┐
                                        │    DefectDojo Vulnerability Manager     │
                                        │ (Centralized Aggregation & SLA Tracking)│
                                        └────────────────────┬────────────────────┘
                                                             │
                                                             ▼
                                        ┌─────────────────────────────────────────┐
                                        │    Elastic SIEM Telemetry Collector     │
                                        │       (devsecops-pipeline-logs)         │
                                        └────────────────────┬────────────────────┘
                                                             │
                                                             ▼
                                        ┌─────────────────────────────────────────┐
                                        │        Slack Automated Incident         │
                                        │             Alert Dispatcher            │
                                        └─────────────────────────────────────────┘

🚀 Key Accomplishments & Technical Features

    Decoupled Reusable Workflow Architecture (security-check.yml)

        Modularized monolithic jobs into parallel, independent execution tracks (sast.yml, secret-scanning.yml, container-sca-sbom.yml, iac-opa.yml, scorecard.yml).

        Dynamically evaluates target branch conditions: enforces strict build-blocking gates (exit-code 1) on main and PRs targeting main, while operating in Advisory Mode (exit-code 0) on feature branches.

    Decoupled Static Code, Quality & Secret Analysis

        Independent Secret Detection (secret-scanning.yml): Runs Gitleaks in parallel with zero dependency on static code analysis, blocking hardcoded API keys, passwords, and private SSH keys with rapid feedback loops.

        Containerized Semgrep SAST (sast.yml): Executes Semgrep via direct Docker invocation to ensure engine stability and bypass third-party action policy restrictions. Detects SQL injection, XSS, and dangerous code patterns while outputting standard SARIF artifacts.

        SonarQube Code Quality Gate (sast.yml): Measures technical debt, code coverage, and quality gate compliance across polyglot codebases.

    Container Security & Software Bill of Materials (SBOM)

        Trivy Container Scan: Evaluates built container images (local-test-image:latest) for high/critical vulnerabilities with ignore-unfixed: true enabled to eliminate unpatchable OS vendor noise.

        SPDX SBOM Generation: Automated creation and artifact upload of standard SPDX SBOM inventories (sbom.spdx.json) for supply chain visibility.

    Policy-as-Code Governance (OPA / Rego)

        Custom Open Policy Agent rules (policies/opa/) validate Infrastructure-as-Code and container configuration files.

        Enforces strict evaluation (opa eval --fail) to block insecure cloud configurations prior to deployment.

    Supply Chain Security & Action Hardening

        Full Commit SHA Pinning: All third-party GitHub Actions across all workflow steps are pinned directly to immutable 40-character commit SHAs to protect against supply chain tampering.

        OpenSSF Scorecard: Automatically evaluates repository posture, top-level token permissions, branch protections, and maintenance health, publishing SARIF reports directly to the GitHub Security tab.

    DefectDojo Centralized Vulnerability Management (defectdojo-ingestion.yml)

        Gates execution on the completion of parallel scan jobs (sast, secret-scanning, container-and-sbom, iac-and-opa).

        Ingests JSON/SARIF artifacts from Gitleaks, Semgrep, Trivy, and OPA directly into DefectDojo.

        Centralizes vulnerability tracking, deduplication, historical trend analysis, and SLA enforcement across organizational repositories.

    Elastic SIEM Telemetry & Security Operations (siem-telemetry.yml)

        Formats pipeline execution metrics into structured JSON telemetry payloads.

        Ships security logs into Elasticsearch / Elastic SIEM (devsecops-pipeline-logs-* index) for real-time SOC monitoring.

    Automated Slack Incident Notifications

        Dispatches formatted real-time alert notifications (PASSED / FAILED) with pipeline metadata and actor details to Slack security channels via incoming webhooks.

📂 Repository Structure
Plaintext

Devsecops-Automation-Engine/
├── .github/
│   └── workflows/
│       ├── container-sca-sbom.yml    # Container scanning & SBOM workflow
│       ├── defectdojo-ingestion.yml  # Centralized DefectDojo ingestion gate
│       ├── delete-actions.yml        # Workflow run cleanup automation
│       ├── iac-opa.yml               # OPA IaC policy enforcement workflow
│       ├── sast.yml                  # Semgrep SAST & SonarQube code quality workflow
│       ├── scorecard.yml             # OpenSSF Scorecard posture workflow
│       ├── secret-scanning.yml       # Gitleaks secret detection workflow
│       ├── security-check.yml        # Main execution & orchestration pipeline
│       └── siem-telemetry.yml        # Elastic SIEM logging workflow
├── policies/
│   └── opa/
│       └── s3_check.rego             # OPA Rego compliance policies
├── src/
│   ├── Dockerfile                    # Container definition
│   └── app.py                        # Application source entrypoint
├── LICENSE                           # MIT Open Source License
├── README.md                         # System documentation
└── SECURITY.md                       # Vulnerability disclosure and security policy

🔑 Required Repository Secrets

To run all pipeline jobs successfully, configure these secrets under Settings → Secrets and variables → Actions:
Secret Name	Description	Example / Scope
SEMGREP_APP_TOKEN	(Optional) Authentication token from Semgrep AppSec	semgrep_...
SONAR_TOKEN	Global analysis authentication token for SonarQube	sqa_...
SONAR_HOST_URL	Endpoint URL for SonarQube server	[https://sonar.your-domain.com](https://sonar.your-domain.com)
DEFECTDOJO_URL	Endpoint URL for DefectDojo instance	[https://defectdojo.your-domain.com](https://defectdojo.your-domain.com)
DEFECTDOJO_API_KEY	User API Key for DefectDojo ingestion	Token 8a9b...
ELASTIC_HOST	Endpoint URL for Elastic SIEM cluster	[https://elastic.your-domain.com:9243](https://elastic.your-domain.com:9243)
ELASTIC_API_KEY	Base64 encoded Elastic API Key for log ingestion	V2...==
SLACK_WEBHOOK_URL	(Optional) Slack Incoming Webhook URL for automated channel alerting	[https://hooks.slack.com/services/](https://hooks.slack.com/services/)...
🛠️ Usage & Integration
Reusing this Engine in Client Repositories

To consume this centralized security engine inside any client repository, create .github/workflows/security-check.yml in your target repo:
YAML

name: Security Check

on:
  push:
    branches: [ "main", "dev" ]
  pull_request:
    branches: [ "main", "dev" ]

jobs:
  run-security-engine:
    uses: Vharse/Devsecops-Automation-Engine/.github/workflows/security-check.yml@main
    permissions:
      contents: read
      security-events: write
      id-token: write
      checks: write
      actions: read
    secrets: inherit
