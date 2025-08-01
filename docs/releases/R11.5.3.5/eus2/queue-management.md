---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:36.937665'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: queue-management.j2 - EUS2
version: '1.0'
---


# Queue Management - EUS2

## Overview

Queue management procedure for **eastus2** region.

### Queue Context

- **Target Region**: EUS2 (eastus2)
- **Queue System**: RabbitMQ
- **Queue Count**: 8

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
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue reports_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue integration_eus2 durable=true
"
ansible eus2_queue -m shell -a "
  rabbitmqctl declare queue analytics_eus2 durable=true
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