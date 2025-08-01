---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:36.191150'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: user-management.j2
title: user-management.j2 - EUS2
version: '1.0'
---


# User Management - EUS2

## Overview

User management procedure for **eastus2** region.

### User Management Context

- **Target Region**: EUS2 (eastus2)
- **Environment**: eus2-production
- **Directory Service**: Active Directory
- **User Groups**: admin, developer, operator

## User Account Management

### Create Service Accounts
```bash
# Create monitoring service account
ansible eus2_all -m user -a "
  name=monitoring
  shell=/bin/bash
  home=/opt/monitoring
  system=yes
  createhome=yes
"

# Create backup service account
ansible eus2_all -m user -a "
  name=backup
  shell=/bin/bash
  home=/opt/backup
  system=yes
  createhome=yes
"

# Create application service account
ansible eus2_app -m user -a "
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
ansible eus2_all -m authorized_key -a "
  user=monitoring
  key='{{ vault_eus2_monitoring_ssh_key }}'
  state=present
"

ansible eus2_all -m authorized_key -a "
  user=backup
  key='{{ vault_eus2_backup_ssh_key }}'
  state=present
"
```

### User Group Management
```bash
# Create operational groups
ansible eus2_all -m group -a "name=operators state=present"
ansible eus2_all -m group -a "name=developers state=present"
ansible eus2_all -m group -a "name=dbadmins state=present"

# Add users to appropriate groups
ansible eus2_all -m user -a "
  name=john.admin
  groups=operators,dbadmins
  append=yes
"
ansible eus2_all -m user -a "
  name=sarah.dev
  groups=developers
  append=yes
"
ansible eus2_all -m user -a "
  name=mike.ops
  groups=operators
  append=yes
"
```

## Access Control

### Sudo Configuration
```bash
# Configure sudo access for operators
ansible eus2_all -m copy -a "
  dest=/etc/sudoers.d/operators
  content='%operators ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker'
  mode=0440
"

# Configure sudo access for developers
ansible eus2_app -m copy -a "
  dest=/etc/sudoers.d/developers
  content='%developers ALL=(appuser) NOPASSWD: ALL'
  mode=0440
"
```

### File Permissions
```bash
# Set application directory permissions
ansible eus2_app -m file -a "
  path=/opt/app
  owner=appuser
  group=developers
  mode=0755
  recurse=yes
"

# Set log directory permissions
ansible eus2_all -m file -a "
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
ansible eus2_all -m lineinfile -a "
  dest=/etc/login.defs
  regexp='^PASS_MAX_DAYS'
  line='PASS_MAX_DAYS 90'
"

# Configure password complexity
ansible eus2_all -m lineinfile -a "
  dest=/etc/security/pwquality.conf
  regexp='^minlen'
  line='minlen = 14'
"
```

### Account Lockout
```bash
# Configure account lockout policy
ansible eus2_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^deny'
  line='deny = 3'
"

ansible eus2_all -m lineinfile -a "
  dest=/etc/security/faillock.conf
  regexp='^unlock_time'
  line='unlock_time = 1800'
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)