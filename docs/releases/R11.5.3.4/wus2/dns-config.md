---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.731564'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# DNS Configuration - WUS2

## Overview

DNS configuration procedure for **westus2** region.

### DNS Context

- **Target Region**: WUS2 (westus2)
- **DNS Provider**: Azure DNS
- **Zone**: example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-wus2 \
  --zone-name example.com \
  --record-set-name www-wus2 \
  --ipv4-address 10.0.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-wus2 \
  --zone-name example.com \
  --record-set-name api-wus2 \
  --ipv4-address 10.0.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-wus2 \
  --zone-name example.com \
  --record-set-name wus2-service \
  --cname wus2.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)