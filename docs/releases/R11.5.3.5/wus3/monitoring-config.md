---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: general
description: MOP documentation for wus3
environment: wus3-production
generated_at: '2025-08-01T08:26:35.865221'
region: wus3
tags:
- wus3
- general
- mop
- ansible
- azure-devops
template_source: monitoring-config.j2
title: monitoring-config.j2 - WUS3
version: '1.0'
---


# Monitoring Configuration - WUS3

## Overview

Monitoring configuration procedure for **westus3** region.

### Monitoring Context

- **Target Region**: WUS3 (westus3)
- **Environment**: wus3-production
- **Monitoring Platform**: Azure Monitor + Grafana
- **Alert Manager**: alert-mgr-wus3.example.com

## Dashboard Configuration

### System Dashboards
- **Infrastructure Overview**: CPU, Memory, Disk usage across all hosts
- **Application Performance**: Response times, error rates, throughput
- **Database Metrics**: Connection pools, query performance, replication lag
- **Network Monitoring**: Bandwidth utilization, packet loss, latency

### Alert Rules
```yaml
alerting_rules:
  - name: high_cpu_usage
    threshold: 85
    duration: 5m
    severity: warning
  - name: disk_space_low
    threshold: 90
    duration: 2m
    severity: critical
  - name: application_down
    threshold: 0
    duration: 1m
    severity: critical
```

## Deployment Steps

### Step 1: Dashboard Deployment
```bash
# Deploy Grafana dashboards
ansible wus3_monitoring -m copy -a "src=dashboards/ dest=/etc/grafana/dashboards/"
ansible wus3_monitoring -m systemd -a "name=grafana-server state=restarted"

# Configure Prometheus targets
ansible wus3_monitoring -m template -a "src=prometheus.yml.j2 dest=/etc/prometheus/prometheus.yml"
ansible wus3_monitoring -m systemd -a "name=prometheus state=restarted"
```

### Step 2: Alert Configuration
```bash
# Deploy alerting rules
ansible wus3_monitoring -m copy -a "src=alert-rules/ dest=/etc/prometheus/rules/"
ansible wus3_monitoring -m systemd -a "name=prometheus state=reloaded"

# Configure notification channels
ansible wus3_monitoring -m template -a "src=alertmanager.yml.j2 dest=/etc/alertmanager/alertmanager.yml"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)