---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:12.236696'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: compliance-audit.j2
title: compliance-audit.j2 - SCUS
version: '1.0'
---


# Compliance Audit - SCUS

## Overview

Compliance audit procedure for **southcentralus** region.

### Audit Context

- **Target Region**: SCUS (southcentralus)
- **Compliance Framework**: SOC2 + ISO27001 + PCI-DSS
- **Audit Date**: 2025-08-01

## Security Compliance

### Access Control Audit
```bash
# Check user account compliance
ansible scus_all -m shell -a "
  awk -F: '(\$3 >= 1000) {print \$1}' /etc/passwd > /tmp/user_audit.txt
"

# Check sudo access
ansible scus_all -m shell -a "
  grep -r '^[^#]' /etc/sudoers.d/ > /tmp/sudo_audit.txt
"

# Check SSH key access
ansible scus_all -m find -a "
  paths=/home
  patterns=authorized_keys
  recurse=yes
" register: ssh_keys
```

### System Hardening Audit
```bash
# Check password policies
ansible scus_all -m shell -a "
  grep -E '^(PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE)' /etc/login.defs
"

# Check firewall status
ansible scus_all -m shell -a "
  iptables -L -n | head -20
"

# Check service exposure
ansible scus_all -m shell -a "
  netstat -tlnp | grep -E ':(22|80|443|3306|5432)'
"
```

## Data Protection Audit

### Encryption Status
```bash
# Check disk encryption
ansible scus_all -m shell -a "
  lsblk -f | grep crypto
"

# Check SSL/TLS configuration
ansible scus_web -m shell -a "
  openssl s_client -connect localhost:443 -brief
"
```

### Backup Verification
```bash
# Check backup schedules
ansible scus_all -m shell -a "
  crontab -l | grep backup
"

# Verify backup integrity
ansible scus_all -m shell -a "
  find /backup -name '*.gz' -mtime -1 | wc -l
"
```

## Audit Report Generation

### Compliance Report
```bash
# Generate compliance report
ansible scus_all -m template -a "
  src=compliance-report.j2
  dest=/tmp/compliance-report-scus-2025-08-01.html
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)