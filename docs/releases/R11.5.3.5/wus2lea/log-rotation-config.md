---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.108735'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: log-rotation-config.j2
title: log-rotation-config.j2 - WUS2LEA
version: '1.0'
---


# Log Rotation Configuration - WUS2LEA

## Overview

Log rotation configuration procedure for **westus2euap** region.

### Log Management Context

- **Target Region**: WUS2LEA (westus2euap)
- **Environment**: wus2lea-production
- **Log Retention**: 60 days
- **Compression**: gzip

## Log Rotation Rules

### System Logs
```bash
# Configure logrotate for system logs
ansible wus2lea_all -m copy -a "
  dest=/etc/logrotate.d/system-logs
  content='
/var/log/messages
/var/log/secure
/var/log/maillog
{
    daily
    rotate 60
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
'
"
```

### Application Logs
```bash
# Configure application log rotation
ansible wus2lea_app -m copy -a "
  dest=/etc/logrotate.d/application
  content='
/opt/app/logs/*.log
{
    daily
    rotate 60
    compress
    delaycompress
    missingok
    notifempty
    create 644 appuser appuser
    postrotate
        systemctl reload application
    endscript
}
'
"
```

### Database Logs
```bash
# Configure database log rotation
ansible wus2lea_db -m copy -a "
  dest=/etc/logrotate.d/mysql
  content='
/var/log/mysql/*.log
{
    daily
    rotate 60
    compress
    delaycompress
    missingok
    notifempty
    create 644 mysql mysql
    postrotate
        systemctl reload mysql
    endscript
}
'
"
```

## Immediate Cleanup

### Manual Log Cleanup
```bash
# Clean up old logs immediately
ansible wus2lea_all -m shell -a "find /var/log -name '*.log' -mtime +60 -delete"
ansible wus2lea_all -m shell -a "find /var/log -name '*.gz' -mtime +60 -delete"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)