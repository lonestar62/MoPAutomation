---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:10.798803'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: log-rotation-config.j2
title: log-rotation-config.j2 - SCUS
version: '1.0'
---


# Log Rotation Configuration - SCUS

## Overview

Log rotation configuration procedure for **southcentralus** region.

### Log Management Context

- **Target Region**: SCUS (southcentralus)
- **Environment**: scus-production
- **Log Retention**: 30 days
- **Compression**: gzip

## Log Rotation Rules

### System Logs
```bash
# Configure logrotate for system logs
ansible scus_all -m copy -a "
  dest=/etc/logrotate.d/system-logs
  content='
/var/log/messages
/var/log/secure
/var/log/maillog
{
    daily
    rotate 30
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
ansible scus_app -m copy -a "
  dest=/etc/logrotate.d/application
  content='
/opt/app/logs/*.log
{
    daily
    rotate 30
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
ansible scus_db -m copy -a "
  dest=/etc/logrotate.d/mysql
  content='
/var/log/mysql/*.log
{
    daily
    rotate 30
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
ansible scus_all -m shell -a "find /var/log -name '*.log' -mtime +30 -delete"
ansible scus_all -m shell -a "find /var/log -name '*.gz' -mtime +30 -delete"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)