---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.628518'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: backup-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Backup Configuration - SCUS

## Overview

Backup configuration procedure for **southcentralus** region.

### Backup Context

- **Target Region**: SCUS (southcentralus)
- **Environment**: scus-production
- **Backup Storage**: backup-storage-scus.blob.core.windows.net
- **Retention Policy**: 30 days

## Backup Components

### Database Backups
```bash
# Configure automated database backups
ansible scus_db -m cron -a "
  name='Daily database backup'
  minute=0
  hour=2
  job='mysqldump --all-databases | gzip > /backup/db-$(date +%Y%m%d).sql.gz'
"

# Configure Azure Blob storage sync
ansible scus_db -m cron -a "
  name='Sync backups to Azure'
  minute=30
  hour=3
  job='az storage blob upload-batch --destination backups --source /backup/'
"
```

### File System Backups
```bash
# System configuration backup
ansible scus_all -m archive -a "
  path=/etc
  dest=/backup/system-config-$(date +%Y%m%d).tar.gz
  format=gz
"

# Application data backup
ansible scus_app -m archive -a "
  path=/opt/app/data
  dest=/backup/app-data-$(date +%Y%m%d).tar.gz
  format=gz
"
```

## Retention Management

### Cleanup Old Backups
```bash
# Remove backups older than retention period
ansible scus_all -m find -a "
  paths=/backup
  age=30d
  file_type=file
" | xargs rm -f
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)