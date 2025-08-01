---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:33.005275'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: config-management.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Configuration Management - WUS2

## Overview

Configuration management procedure for **westus2** region.

### Configuration Context

- **Target Region**: WUS2 (westus2)
- **Config Version**: 2.1.0
- **Management Tool**: Ansible

## System Configuration

### Network Configuration
```bash
# Update network settings
ansible wus2_all -m lineinfile -a "
  dest=/etc/sysctl.conf
  regexp='^net.ipv4.ip_forward'
  line='net.ipv4.ip_forward = 0'
"

# Update DNS configuration
ansible wus2_all -m template -a "
  src=resolv.conf.j2
  dest=/etc/resolv.conf
"
```

### Time Synchronization
```bash
# Configure NTP
ansible wus2_all -m template -a "
  src=ntp.conf.j2
  dest=/etc/ntp.conf
"

ansible wus2_all -m systemd -a "name=ntp state=restarted"
```

## Application Configuration

### Environment Variables
```bash
# Update application environment
ansible wus2_app -m template -a "
  src=app-env.j2
  dest=/opt/app/.env
"

# Restart application services
ansible wus2_app -m systemd -a "name=application state=restarted"
```

### Database Configuration
```bash
# Update database configuration
ansible wus2_db -m template -a "
  src=mysql.cnf.j2
  dest=/etc/mysql/mysql.conf.d/mysqld.cnf
"

ansible wus2_db -m systemd -a "name=mysql state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)