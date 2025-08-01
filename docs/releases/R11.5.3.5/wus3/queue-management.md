---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:26:36.963564'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: queue-management.j2
title: queue-management.j2 - WUS3
version: '1.0'
---


# Queue Management - WUS3

## Overview

Queue management procedure for **westus3** region.

### Queue Context

- **Target Region**: WUS3 (westus3)
- **Queue System**: RabbitMQ
- **Queue Count**: 12

## Queue Configuration

### RabbitMQ Setup
```bash
# Configure RabbitMQ virtual hosts
ansible wus3_queue -m shell -a "
  rabbitmqctl add_vhost wus3-production
"

# Create queues
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue email_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue notification_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue processing_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue audit_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue backup_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue reports_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue integration_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue analytics_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue ml-training_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue data-pipeline_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue real-time_wus3 durable=true
"
ansible wus3_queue -m shell -a "
  rabbitmqctl declare queue streaming_wus3 durable=true
"

# Configure queue policies
ansible wus3_queue -m shell -a "
  rabbitmqctl set_policy ha-all '.*' '{\"ha-mode\":\"all\"}'
"
```

### Worker Configuration
```bash
# Update worker configuration
ansible wus3_worker -m template -a "
  src=worker-config.j2
  dest=/opt/worker/config/worker.conf
"

# Restart worker services
ansible wus3_worker -m systemd -a "name=worker state=restarted"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)