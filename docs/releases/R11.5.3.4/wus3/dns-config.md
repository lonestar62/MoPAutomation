---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.732757'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# DNS Configuration - WUS3

## Overview

DNS configuration procedure for **westus3** region.

### DNS Context

- **Target Region**: WUS3 (westus3)
- **DNS Provider**: Azure DNS
- **Zone**: example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-wus3 \
  --zone-name example.com \
  --record-set-name www-wus3 \
  --ipv4-address 10.0.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-wus3 \
  --zone-name example.com \
  --record-set-name api-wus3 \
  --ipv4-address 10.0.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-wus3 \
  --zone-name example.com \
  --record-set-name wus3-service \
  --cname wus3.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)