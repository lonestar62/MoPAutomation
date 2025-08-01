---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.692011'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: user-management.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# User Management - WUS2

## Overview

User management procedure for **westus2** region.

### User Management Context

- **Target Region**: WUS2 (westus2)
- **Environment**: wus2-production
- **Directory Service**: Active Directory
- **User Groups**: admin, developer, operator

## User Account Management

### Create Service Accounts
```bash
# Create monitoring service account
ansible wus2_all -m user -a "
  name=monitoring
  shell=/bin/bash
  home=/opt/monitoring
  system=yes
  createhome=yes
"

# Create backup service account
ansible wus2_all -m user -a "
  name=backup
  shell=/bin/bash
  home=/opt/backup
  system=yes
  createhome=yes
"

# Create application service account
ansible wus2_app -m user -a "
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
ansible wus2_all -m authorized_key -a "
  user=monitoring
  key=''
  state=present
"

ansible wus2_all -m authorized_key -a "
  user=backup
  key=''
  state=present
"
```

### User Group Management
```bash
# Create operational groups
ansible wus2_all -m group -a "name=operators state=present"
ansible wus2_all -m group -a "name=developers state=present"
ansible wus2_all -m group -a "name=dbadmins state=present"

# Add users to appropriate groups
```

## Access Control

### Sudo Configuration
```bash
# Configure sudo access for operators
ansible wus2_all -m copy -a "
  dest=/etc/sudoers.d/operators
  content='%operators ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker'
  mode=0440
"

# Configure sudo access for developers
ansible wus2_app -m copy -a "
  dest=/etc/sudoers.d/developers
  content='%developers ALL=(appuser) NOPASSWD: ALL'
  mode=0440
"
```

### File Permissions
```bash
# Set application directory permissions
ansible wus2_app -m file -a "
  path=/opt/app
  owner=appuser
  group=developers
  mode=0755
  recurse=yes
"

# Set log directory permissions
ansible wus2_all -m file -a "
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
ansible wus2_all -m lineinfile -a "
  dest=/etc/login.defs
  regexp='^PASS_MAX_DAYS'
  line='PASS_MAX_DAYS 90'
"

# Configure password complexity
ansible wus2_all -m lineinfile -a "
  dest=/etc/security/pwquality.conf
  regexp='^minlen'
  line='minlen = 12'
"
```

### Account Lockout
```bash
# Configure account lockout policy
ansible wus2_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^deny'
  line='deny = 5'
"

ansible wus2_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^unlock_time'
  line='unlock_time = 900'
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)