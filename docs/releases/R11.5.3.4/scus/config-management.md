---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:33.011300'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: config-management.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Configuration Management - SCUS

## Overview

Configuration management procedure for **southcentralus** region.

### Configuration Context

- **Target Region**: SCUS (southcentralus)
- **Config Version**: 2.1.0
- **Management Tool**: Ansible

## System Configuration

### Network Configuration
```bash
# Update network settings
ansible scus_all -m lineinfile -a "
  dest=/etc/sysctl.conf
  regexp='^net.ipv4.ip_forward'
  line='net.ipv4.ip_forward = 0'
"

# Update DNS configuration
ansible scus_all -m template -a "
  src=resolv.conf.j2
  dest=/etc/resolv.conf
"
```

### Time Synchronization
```bash
# Configure NTP
ansible scus_all -m template -a "
  src=ntp.conf.j2
  dest=/etc/ntp.conf
"

ansible scus_all -m systemd -a "name=ntp state=restarted"
```

## Application Configuration

### Environment Variables
```bash
# Update application environment
ansible scus_app -m template -a "
  src=app-env.j2
  dest=/opt/app/.env
"

# Restart application services
ansible scus_app -m systemd -a "name=application state=restarted"
```

### Database Configuration
```bash
# Update database configuration
ansible scus_db -m template -a "
  src=mysql.cnf.j2
  dest=/etc/mysql/mysql.conf.d/mysqld.cnf
"

ansible scus_db -m systemd -a "name=mysql state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)