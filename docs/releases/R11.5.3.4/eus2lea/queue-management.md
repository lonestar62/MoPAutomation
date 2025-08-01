---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.925724'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# Queue Management - EUS2LEA

## Overview

Queue management procedure for **eastus2euap** region.

### Queue Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Queue System**: RabbitMQ
- **Queue Count**: 5

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible eus2lea_queue -m shell -a "
  rabbitmqctl add_vhost eus2lea-production
"

# Create queues
ansible eus2lea_queue -m shell -a "
  rabbitmqctl declare queue email_eus2lea durable=true
"
ansible eus2lea_queue -m shell -a "
  rabbitmqctl declare queue notification_eus2lea durable=true
"
ansible eus2lea_queue -m shell -a "
  rabbitmqctl declare queue processing_eus2lea durable=true
"
ansible eus2lea_queue -m shell -a "
  rabbitmqctl declare queue audit_eus2lea durable=true
"
ansible eus2lea_queue -m shell -a "
  rabbitmqctl declare queue backup_eus2lea durable=true
"

# Configure queue policies
ansible eus2lea_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible eus2lea_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible eus2lea_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)