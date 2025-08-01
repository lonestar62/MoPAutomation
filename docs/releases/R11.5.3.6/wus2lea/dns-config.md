---
ado_organization: '{ vault_wus2lea_ado_organization }'
azure_region: westus2euap
category: general
description: MOP documentation for wus2lea
early_access: true
environment: wus2lea-production
generated_at: '2025-08-01T08:27:11.193254'
preview_features: true
region: wus2lea
tags:
- wus2lea
- general
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: dns-config.j2 - WUS2LEA
version: '1.0'
---


# DNS Configuration - WUS2LEA

## Overview

DNS configuration procedure for **westus2euap** region.

### DNS Context

- **Target Region**: WUS2LEA (westus2euap)
- **DNS Provider**: Azure DNS
- **Zone**: wus2lea.example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-wus2lea \
  --zone-name wus2lea.example.com \
  --record-set-name www-wus2lea \
  --ipv4-address 10.5.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-wus2lea \
  --zone-name wus2lea.example.com \
  --record-set-name api-wus2lea \
  --ipv4-address 10.5.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-wus2lea \
  --zone-name wus2lea.example.com \
  --record-set-name wus2lea-service \
  --cname wus2lea.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: WUS2LEA (westus2euap)