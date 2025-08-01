---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.627233'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: backup-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# Backup Configuration - WUS3

## Overview

Backup configuration procedure for **westus3** region.

### Backup Context

- **Target Region**: WUS3 (westus3)
- **Environment**: wus3-production
- **Backup Storage**: backup-storage-wus3.blob.core.windows.net
- **Retention Policy**: 30 days

## Backup Components

### Database Backups
```bash
# Configure automated database backups
ansible wus3_db -m cron -a "
  name='Daily database backup'
  minute=0
  hour=2
  job='mysqldump --all-databases | gzip > /backup/db-$(date +%Y%m%d).sql.gz'
"

# Configure Azure Blob storage sync
ansible wus3_db -m cron -a "
  name='Sync backups to Azure'
  minute=30
  hour=3
  job='az storage blob upload-batch --destination backups --source /backup/'
"
```

### File System Backups
```bash
# System configuration backup
ansible wus3_all -m archive -a "
  path=/etc
  dest=/backup/system-config-$(date +%Y%m%d).tar.gz
  format=gz
"

# Application data backup
ansible wus3_app -m archive -a "
  path=/opt/app/data
  dest=/backup/app-data-$(date +%Y%m%d).tar.gz
  format=gz
"
```

## Retention Management

### Cleanup Old Backups
```bash
# Remove backups older than retention period
ansible wus3_all -m find -a "
  paths=/backup
  age=30d
  file_type=file
" | xargs rm -f
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)