---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.653677'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: log-rotation-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# Log Rotation Configuration - WUS3

## Overview

Log rotation configuration procedure for **westus3** region.

### Log Management Context

- **Target Region**: WUS3 (westus3)
- **Environment**: wus3-production
- **Log Retention**: 14 days
- **Compression**: gzip

## Log Rotation Rules

### System Logs
```bash
# Configure logrotate for system logs
ansible wus3_all -m copy -a "
  dest=/etc/logrotate.d/system-logs
  content='
/var/log/messages
/var/log/secure
/var/log/maillog
{
    daily
    rotate 14
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
ansible wus3_app -m copy -a "
  dest=/etc/logrotate.d/application
  content='
/opt/app/logs/*.log
{
    daily
    rotate 14
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
ansible wus3_db -m copy -a "
  dest=/etc/logrotate.d/mysql
  content='
/var/log/mysql/*.log
{
    daily
    rotate 14
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
ansible wus3_all -m shell -a "find /var/log -name '*.log' -mtime +14 -delete"
ansible wus3_all -m shell -a "find /var/log -name '*.gz' -mtime +14 -delete"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)