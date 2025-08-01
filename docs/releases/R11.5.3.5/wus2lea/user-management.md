---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.244682'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: user-management.j2
title: user-management.j2 - WUS2LEA
version: '1.0'
---


# User Management - WUS2LEA

## Overview

User management procedure for **westus2euap** region.

### User Management Context

- **Target Region**: WUS2LEA (westus2euap)
- **Environment**: wus2lea-production
- **Directory Service**: Active Directory
- **User Groups**: admin, developer, operator

## User Account Management

### Create Service Accounts
```bash
# Create monitoring service account
ansible wus2lea_all -m user -a "
  name=monitoring
  shell=/bin/bash
  home=/opt/monitoring
  system=yes
  createhome=yes
"

# Create backup service account
ansible wus2lea_all -m user -a "
  name=backup
  shell=/bin/bash
  home=/opt/backup
  system=yes
  createhome=yes
"

# Create application service account
ansible wus2lea_app -m user -a "
  name=appuser
  shell=/bin/bash
  home=/opt/app
  system=yes
  createhome=yes
"
```

### Configure SSH Keys
```bash
# Deploy SSH keys for service accounts
ansible wus2lea_all -m authorized_key -a "
  user=monitoring
  key='{{ vault_wus2lea_monitoring_ssh_key }}'
  state=present
"

ansible wus2lea_all -m authorized_key -a "
  user=backup
  key='{{ vault_wus2lea_backup_ssh_key }}'
  state=present
"
```

### User Group Management
```bash
# Create operational groups
ansible wus2lea_all -m group -a "name=operators state=present"
ansible wus2lea_all -m group -a "name=developers state=present"
ansible wus2lea_all -m group -a "name=dbadmins state=present"

# Add users to appropriate groups
ansible wus2lea_all -m user -a "
  name=alex.admin
  groups=operators,dbadmins,early-access
  append=yes
"
ansible wus2lea_all -m user -a "
  name=zoe.dev
  groups=developers,early-access
  append=yes
"
ansible wus2lea_all -m user -a "
  name=max.ops
  groups=operators,early-access
  append=yes
"
```

## Access Control

### Sudo Configuration
```bash
# Configure sudo access for operators
ansible wus2lea_all -m copy -a "
  dest=/etc/sudoers.d/operators
  content='%operators ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker'
  mode=0440
"

# Configure sudo access for developers
ansible wus2lea_app -m copy -a "
  dest=/etc/sudoers.d/developers
  content='%developers ALL=(appuser) NOPASSWD: ALL'
  mode=0440
"
```

### File Permissions
```bash
# Set application directory permissions
ansible wus2lea_app -m file -a "
  path=/opt/app
  owner=appuser
  group=developers
  mode=0755
  recurse=yes
"

# Set log directory permissions
ansible wus2lea_all -m file -a "
  path=/var/log/application
  owner=appuser
  group=operators
  mode=0750
  state=directory
"
```

## Security Hardening

### Password Policies
```bash
# Configure password aging
ansible wus2lea_all -m lineinfile -a "
  dest=/etc/login.defs
  regexp='^PASS_MAX_DAYS'
  line='PASS_MAX_DAYS 60'
"

# Configure password complexity
ansible wus2lea_all -m lineinfile -a "
  dest=/etc/security/pwquality.conf
  regexp='^minlen'
  line='minlen = 16'
"
```

### Account Lockout
```bash
# Configure account lockout policy
ansible wus2lea_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^deny'
  line='deny = 2'
"

ansible wus2lea_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^unlock_time'
  line='unlock_time = 3600'
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)