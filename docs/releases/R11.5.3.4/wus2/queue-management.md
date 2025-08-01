---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.918688'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# Queue Management - WUS2

## Overview

Queue management procedure for **westus2** region.

### Queue Context

- **Target Region**: WUS2 (westus2)
- **Queue System**: RabbitMQ
- **Queue Count**: 5

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible wus2_queue -m shell -a "
  rabbitmqctl add_vhost wus2-production
"

# Create queues
ansible wus2_queue -m shell -a "
  rabbitmqctl declare queue email_wus2 durable=true
"
ansible wus2_queue -m shell -a "
  rabbitmqctl declare queue notification_wus2 durable=true
"
ansible wus2_queue -m shell -a "
  rabbitmqctl declare queue processing_wus2 durable=true
"
ansible wus2_queue -m shell -a "
  rabbitmqctl declare queue audit_wus2 durable=true
"
ansible wus2_queue -m shell -a "
  rabbitmqctl declare queue backup_wus2 durable=true
"

# Configure queue policies
ansible wus2_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible wus2_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible wus2_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)