---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:18:32.928152'
preview_features: true
region: wus2lea
tags:
- wus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: Monitoring Agent Upgrade - WUS2LEA
version: 1.2.0
---


# Queue Management - WUS2LEA

## Overview

Queue management procedure for **westus2euap** region.

### Queue Context

- **Target Region**: WUS2LEA (westus2euap)
- **Queue System**: RabbitMQ
- **Queue Count**: 5

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible wus2lea_queue -m shell -a "
  rabbitmqctl add_vhost wus2lea-production
"

# Create queues
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue email_wus2lea durable=true
"
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue notification_wus2lea durable=true
"
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue processing_wus2lea durable=true
"
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue audit_wus2lea durable=true
"
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue backup_wus2lea durable=true
"

# Configure queue policies
ansible wus2lea_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible wus2lea_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible wus2lea_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)