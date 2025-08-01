---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:26:35.952395'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: backup-config.j2
title: backup-config.j2 - EUS2LEA
version: '1.0'
---


# Backup Configuration - EUS2LEA

## Overview

Backup configuration procedure for **eastus2euap** region.

### Backup Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Environment**: eus2lea-production
- **Backup Storage**: backup-storage-eus2lea.blob.core.windows.net
- **Retention Policy**: 180 days

## Backup Components

### Database Backups
```bash
# Configure automated database backups
ansible eus2lea_db -m cron -a "
  name='Daily database backup'
  minute=0
  hour=2
  job='mysqldump --all-databases | gzip > /backup/db-$(date +%Y%m%d).sql.gz'
"

# Configure Azure Blob storage sync
ansible eus2lea_db -m cron -a "
  name='Sync backups to Azure'
  minute=30
  hour=3
  job='az storage blob upload-batch --destination backups --source /backup/'
"
```

### File System Backups
```bash
# System configuration backup
ansible eus2lea_all -m archive -a "
  path=/etc
  dest=/backup/system-config-$(date +%Y%m%d).tar.gz
  format=gz
"

# Application data backup
ansible eus2lea_app -m archive -a "
  path=/opt/app/data
  dest=/backup/app-data-$(date +%Y%m%d).tar.gz
  format=gz
"
```

## Retention Management

### Cleanup Old Backups
```bash
# Remove backups older than retention period
ansible eus2lea_all -m find -a "
  paths=/backup
  age=180d
  file_type=file
" | xargs rm -f
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)