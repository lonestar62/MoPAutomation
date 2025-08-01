---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:26:36.996349'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: queue-management.j2 - WUS2LEA
version: '1.0'
---


# Queue Management - WUS2LEA

## Overview

Queue management procedure for **westus2euap** region.

### Queue Context

- **Target Region**: WUS2LEA (westus2euap)
- **Queue System**: RabbitMQ
- **Queue Count**: 6

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
ansible wus2lea_queue -m shell -a "
  rabbitmqctl declare queue preview-features_wus2lea durable=true
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