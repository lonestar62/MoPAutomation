---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:27:11.324350'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: storage-config.j2
title: storage-config.j2 - WUS3
version: '1.0'
---


# Storage Configuration - WUS3

## Overview

Storage configuration procedure for **westus3** region.

### Storage Context

- **Target Region**: WUS3 (westus3)
- **Storage Account**: storagewus3
- **File System**: xfs

## Storage Volume Configuration

### Disk Mounting
```bash
# Create mount points
ansible wus3_all -m file -a "
  path=/opt/data
  state=directory
  mode=0755
"

# Mount storage volumes
ansible wus3_all -m mount -a "
  path=/opt/data
  src=/dev/nvme0n1p1
  fstype=xfs
  state=mounted
"

# Update fstab for persistence
ansible wus3_all -m lineinfile -a "
  dest=/etc/fstab
  line='/dev/nvme0n1p1 /opt/data xfs defaults 0 2'
"
```

### Permissions Setup
```bash
# Set storage permissions
ansible wus3_all -m file -a "
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
**Region**: WUS3 (westus3)