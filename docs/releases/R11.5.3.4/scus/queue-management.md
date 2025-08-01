---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.923213'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# Queue Management - SCUS

## Overview

Queue management procedure for **southcentralus** region.

### Queue Context

- **Target Region**: SCUS (southcentralus)
- **Queue System**: RabbitMQ
- **Queue Count**: 5

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible scus_queue -m shell -a "
  rabbitmqctl add_vhost scus-production
"

# Create queues
ansible scus_queue -m shell -a "
  rabbitmqctl declare queue email_scus durable=true
"
ansible scus_queue -m shell -a "
  rabbitmqctl declare queue notification_scus durable=true
"
ansible scus_queue -m shell -a "
  rabbitmqctl declare queue processing_scus durable=true
"
ansible scus_queue -m shell -a "
  rabbitmqctl declare queue audit_scus durable=true
"
ansible scus_queue -m shell -a "
  rabbitmqctl declare queue backup_scus durable=true
"

# Configure queue policies
ansible scus_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible scus_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible scus_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)