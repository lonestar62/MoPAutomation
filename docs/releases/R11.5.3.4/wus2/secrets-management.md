---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.790038'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: secrets-management.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Secrets Management - WUS2

## Overview

Secrets management procedure for **westus2** region.

### Secrets Context

- **Target Region**: WUS2 (westus2)
- **Key Vault**: kv-wus2
- **Rotation Schedule**: Quarterly

## Secret Rotation

### Database Credentials
```bash
# Generate new database password
NEW_DB_PASSWORD=$(openssl rand -base64 32)

# Update password in Key Vault
az keyvault secret set \
  --vault-name kv-wus2 \
  --name db-password \
  --value "$NEW_DB_PASSWORD"

# Update application configuration
ansible wus2_app -m replace -a "
  dest=/opt/app/config/database.conf
  regexp='password=.*'
  replace='password={{ vault_db_password }}'
"
```

### API Keys
```bash
# Rotate API keys
NEW_API_KEY=$(uuidgen)
az keyvault secret set \
  --vault-name kv-wus2 \
  --name api-key \
  --value "$NEW_API_KEY"

# Update service configurations
ansible wus2_web -m template -a "
  src=api-config.j2
  dest=/opt/web/config/api.conf
"
```

### SSL Certificates
```bash
# Update SSL certificate secrets
ansible wus2_web -m copy -a "
  src=/tmp/new-cert.pem
  dest=/etc/ssl/certs/server.crt
  mode=0644
"

ansible wus2_web -m copy -a "
  src=/tmp/new-key.pem
  dest=/etc/ssl/private/server.key
  mode=0600
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)