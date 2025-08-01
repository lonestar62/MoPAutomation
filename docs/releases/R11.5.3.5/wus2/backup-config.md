---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:26:35.917468'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: backup-config.j2
title: backup-config.j2 - WUS2
version: '1.0'
---


# Backup Configuration - WUS2

## Overview

Backup configuration procedure for **westus2** region.

### Backup Context

- **Target Region**: WUS2 (westus2)
- **Environment**: wus2-production
- **Backup Storage**: backup-storage-wus2.blob.core.windows.net
- **Retention Policy**: 90 days

## Backup Components

### Database Backups
```bash
# Configure automated database backups
ansible wus2_db -m cron -a "
  name='Daily database backup'
  minute=0
  hour=2
  job='mysqldump --all-databases | gzip > /backup/db-$(date +%Y%m%d).sql.gz'
"

# Configure Azure Blob storage sync
ansible wus2_db -m cron -a "
  name='Sync backups to Azure'
  minute=30
  hour=3
  job='az storage blob upload-batch --destination backups --source /backup/'
"
```

### File System Backups
```bash
# System configuration backup
ansible wus2_all -m archive -a "
  path=/etc
  dest=/backup/system-config-$(date +%Y%m%d).tar.gz
  format=gz
"

# Application data backup
ansible wus2_app -m archive -a "
  path=/opt/app/data
  dest=/backup/app-data-$(date +%Y%m%d).tar.gz
  format=gz
"
```

## Retention Management

### Cleanup Old Backups
```bash
# Remove backups older than retention period
ansible wus2_all -m find -a "
  paths=/backup
  age=90d
  file_type=file
" | xargs rm -f
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)