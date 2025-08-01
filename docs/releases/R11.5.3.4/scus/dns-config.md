---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: scus-production
generated_at: '2025-08-01T08:18:32.733932'
region: scus
tags:
- scus
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: Monitoring Agent Upgrade - SCUS
version: 1.2.0
---


# DNS Configuration - SCUS

## Overview

DNS configuration procedure for **southcentralus** region.

### DNS Context

- **Target Region**: SCUS (southcentralus)
- **DNS Provider**: Azure DNS
- **Zone**: example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-scus \
  --zone-name example.com \
  --record-set-name www-scus \
  --ipv4-address 10.0.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-scus \
  --zone-name example.com \
  --record-set-name api-scus \
  --ipv4-address 10.0.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-scus \
  --zone-name example.com \
  --record-set-name scus-service \
  --cname scus.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)