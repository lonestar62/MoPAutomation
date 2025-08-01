---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.794247'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: secrets-management.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Secrets Management - SCUS

## Overview

Secrets management procedure for **southcentralus** region.

### Secrets Context

- **Target Region**: SCUS (southcentralus)
- **Key Vault**: kv-scus
- **Rotation Schedule**: Quarterly

## Secret Rotation

### Database Credentials
```bash
# Generate new database password
NEW_DB_PASSWORD=$(openssl rand -base64 32)

# Update password in Key Vault
az keyvault secret set \
  --vault-name kv-scus \
  --name db-password \
  --value "$NEW_DB_PASSWORD"

# Update application configuration
ansible scus_app -m replace -a "
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
  --vault-name kv-scus \
  --name api-key \
  --value "$NEW_API_KEY"

# Update service configurations
ansible scus_web -m template -a "
  src=api-config.j2
  dest=/opt/web/config/api.conf
"
```

### SSL Certificates
```bash
# Update SSL certificate secrets
ansible scus_web -m copy -a "
  src=/tmp/new-cert.pem
  dest=/etc/ssl/certs/server.crt
  mode=0644
"

ansible scus_web -m copy -a "
  src=/tmp/new-key.pem
  dest=/etc/ssl/private/server.key
  mode=0600
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)