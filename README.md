# Maroon Onitas

**Sovereign Pillar: `onitas`** | **Pod: economy** | **Wave: 7**

---

## Overview

Onitas Market — companion marketplace with extended vendor network.

This pillar is part of the **Maroon 37-Pillar Sovereign Mesh** as defined in the MAROON_MASTER_CODEX.

## Codex Compliance

| Requirement | Status |
|-------------|--------|
| config.yaml | Implemented |
| agent-contract.yaml | Implemented |
| audit.yml | Implemented |
| main.py (MIVL handshake) | Implemented |
| Terraform (BigQuery + GCS + Pub/Sub) | Implemented |
| CI/CD (GitHub Actions) | Implemented |
| Event Bus (no direct calls) | Enforced |
| Fail-Closed Mode | Enforced |

## Structure

```
Onitas-market-/
-- config.yaml              <- Pillar identity (Codex DNA)
-- agent-contract.yaml       <- MIVL + security contract
-- audit.yml                 <- Audit gate definition
-- main.py                   <- Sovereign node initializer
-- frontend/
|  -- index.html             <- UI application
-- terraform/
|  -- main.tf                <- GCP infrastructure (BigQuery, GCS, Pub/Sub, IAM)
-- .github/
|  -- workflows/
|     -- audit.yml           <- CI/CD: MIVL handshake + TF validate
-- README.md
```

## Quick Start

```bash
# 1. Verify sovereign identity
python main.py

# 2. Deploy infrastructure
cd terraform
terraform init
terraform plan -var="project_id=YOUR_PROJECT_ID"
terraform apply

# 3. Open frontend
open frontend/index.html
```

## Sovereignty Laws

- **FAIL-CLOSED**: main.py exits code 1 if MIVL handshake fails
- **TRUTH-ANCHORED**: Every transaction hashed SHA-512 to the Truth-Teller ledger
- **EVENT-DRIVEN**: No direct pillar calls. All communication via Pub/Sub Event Bus
- **NASA-GRADE**: No deployment without audit.yml gate

---

*Part of the Maroon Sovereign Infrastructure. The architecture is sovereign.*
