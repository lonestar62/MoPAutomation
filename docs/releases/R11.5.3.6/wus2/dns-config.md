---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: general
description: MOP documentation for wus2
environment: wus2-production
generated_at: '2025-08-01T08:27:11.146144'
region: wus2
tags:
- wus2
- general
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: dns-config.j2 - WUS2
version: '1.0'
---


# DNS Configuration - WUS2

## Overview

DNS configuration procedure for **westus2** region.

### DNS Context

- **Target Region**: WUS2 (westus2)
- **DNS Provider**: Azure DNS
- **Zone**: wus2.example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-wus2 \
  --zone-name wus2.example.com \
  --record-set-name www-wus2 \
  --ipv4-address 10.1.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-wus2 \
  --zone-name wus2.example.com \
  --record-set-name api-wus2 \
  --ipv4-address 10.1.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-wus2 \
  --zone-name wus2.example.com \
  --record-set-name wus2-service \
  --cname wus2.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)