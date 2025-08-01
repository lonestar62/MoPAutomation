---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:27:10.583079'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: backup-config.j2
title: backup-config.j2 - EUS2
version: '1.0'
---


# Backup Configuration - EUS2

## Overview

Backup configuration procedure for **eastus2** region.

### Backup Context

- **Target Region**: EUS2 (eastus2)
- **Environment**: eus2-production
- **Backup Storage**: backup-storage-eus2.blob.core.windows.net
- **Retention Policy**: 90 days

## Backup Components

### Database Backups
```bash
# Configure automated database backups
ansible eus2_db -m cron -a "
  name='Daily database backup'
  minute=0
  hour=2
  job='mysqldump --all-databases | gzip > /backup/db-$(date +%Y%m%d).sql.gz'
"

# Configure Azure Blob storage sync
ansible eus2_db -m cron -a "
  name='Sync backups to Azure'
  minute=30
  hour=3
  job='az storage blob upload-batch --destination backups --source /backup/'
"
```

### File System Backups
```bash
# System configuration backup
ansible eus2_all -m archive -a "
  path=/etc
  dest=/backup/system-config-$(date +%Y%m%d).tar.gz
  format=gz
"

# Application data backup
ansible eus2_app -m archive -a "
  path=/opt/app/data
  dest=/backup/app-data-$(date +%Y%m%d).tar.gz
  format=gz
"
```

## Retention Management

### Cleanup Old Backups
```bash
# Remove backups older than retention period
ansible eus2_all -m find -a "
  paths=/backup
  age=90d
  file_type=file
" | xargs rm -f
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)