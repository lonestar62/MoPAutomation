---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:26:36.513214'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: storage-config.j2 - WUS2
version: '1.0'
---


# Storage Configuration - WUS2

## Overview

Storage configuration procedure for **westus2** region.

### Storage Context

- **Target Region**: WUS2 (westus2)
- **Storage Account**: storagewus2
- **File System**: ext4

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible wus2_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible wus2_all -m mount -a "
  path=/opt/data
  src=/dev/sdb1
  fstype=ext4
  state=mounted
"

# Update fstab for persistence
ansible wus2_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/sdb1 /opt/data ext4 defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible wus2_all -m file -a "
  path=/opt/data
  owner=appuser
  group=appgroup
  mode=0755
  recurse=yes
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)