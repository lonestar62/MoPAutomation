---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: eus2-production
generated_at: '2025-08-01T08:18:32.915485'
region: eus2
tags:
- eus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: Monitoring Agent Upgrade - EUS2
version: 1.2.0
---


# Queue Management - EUS2

## Overview

Queue management procedure for **eastus2** region.

### Queue Context

- **Target Region**: EUS2 (eastus2)
- **Queue System**: RabbitMQ
- **Queue Count**: 5

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible eus2_queue -m shell -a "
  rabbitmqctl add_vhost eus2-production
"

# Create queues
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue email_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue notification_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue processing_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue audit_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue backup_eus2 durable=true
"

# Configure queue policies
ansible eus2_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible eus2_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible eus2_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)