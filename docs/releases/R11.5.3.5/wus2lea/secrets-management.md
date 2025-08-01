---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.701490'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: secrets-management.j2
title: secrets-management.j2 - WUS2LEA
version: '1.0'
---


# Secrets Management - WUS2LEA

## Overview

Secrets management procedure for **westus2euap** region.

### Secrets Context

- **Target Region**: WUS2LEA (westus2euap)
- **Key Vault**: kv-wus2lea
- **Rotation Schedule**: Monthly

## Secret Rotation

### Database Credentials
```bash
# Generate new database password
NEW_DB_PASSWORD=$(openssl rand -base64 32)

# Update password in Key Vault
az keyvault secret set \
  --vault-name kv-wus2lea \
  --name db-password \
  --value "$NEW_DB_PASSWORD"

# Update application configuration
ansible wus2lea_app -m replace -a "
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
  --vault-name kv-wus2lea \
  --name api-key \
  --value "$NEW_API_KEY"

# Update service configurations
ansible wus2lea_web -m template -a "
  src=api-config.j2
  dest=/opt/web/config/api.conf
"
```

### SSL Certificates
```bash
# Update SSL certificate secrets
ansible wus2lea_web -m copy -a "
  src=/etc/ssl/certs/wus2lea-server.crt
  dest=/etc/ssl/certs/server.crt
  mode=0644
"

ansible wus2lea_web -m copy -a "
  src=/etc/ssl/private/wus2lea-server.key
  dest=/etc/ssl/private/server.key
  mode=0600
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)