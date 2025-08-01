---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:27:12.264180'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: compliance-audit.j2
title: compliance-audit.j2 - WUS2LEA
version: '1.0'
---


# Compliance Audit - WUS2LEA

## Overview

Compliance audit procedure for **westus2euap** region.

### Audit Context

- **Target Region**: WUS2LEA (westus2euap)
- **Compliance Framework**: SOC2 + ISO27001 + PCI-DSS + Early Access
- **Audit Date**: 2025-08-01

## Security Compliance

### Access Control Audit
```bash
# Check user account compliance
ansible wus2lea_all -m shell -a "
  awk -F: '(\$3 >= 1000) {print \$1}' /etc/passwd > /tmp/user_audit.txt
"

# Check sudo access
ansible wus2lea_all -m shell -a "
  grep -r '^[^#]' /etc/sudoers.d/ > /tmp/sudo_audit.txt
"

# Check SSH key access
ansible wus2lea_all -m find -a "
  paths=/home
  patterns=authorized_keys
  recurse=yes
" register: ssh_keys
```

### System Hardening Audit
```bash
# Check password policies
ansible wus2lea_all -m shell -a "
  grep -E '^(PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE)' /etc/login.defs
"

# Check firewall status
ansible wus2lea_all -m shell -a "
  iptables -L -n | head -20
"

# Check service exposure
ansible wus2lea_all -m shell -a "
  netstat -tlnp | grep -E ':(22|80|443|3306|5432)'
"
```

## Data Protection Audit

### Encryption Status
```bash
# Check disk encryption
ansible wus2lea_all -m shell -a "
  lsblk -f | grep crypto
"

# Check SSL/TLS configuration
ansible wus2lea_web -m shell -a "
  openssl s_client -connect localhost:443 -brief
"
```

### Backup Verification
```bash
# Check backup schedules
ansible wus2lea_all -m shell -a "
  crontab -l | grep backup
"

# Verify backup integrity
ansible wus2lea_all -m shell -a "
  find /backup -name '*.gz' -mtime -1 | wc -l
"
```

## Audit Report Generation

### Compliance Report
```bash
# Generate compliance report
ansible wus2lea_all -m template -a "
  src=compliance-report.j2
  dest=/tmp/compliance-report-wus2lea-2025-08-01.html
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)