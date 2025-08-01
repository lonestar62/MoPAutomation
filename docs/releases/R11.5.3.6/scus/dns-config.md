---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:11.170377'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: dns-config.j2
title: dns-config.j2 - SCUS
version: '1.0'
---


# DNS Configuration - SCUS

## Overview

DNS configuration procedure for **southcentralus** region.

### DNS Context

- **Target Region**: SCUS (southcentralus)
- **DNS Provider**: Azure DNS
- **Zone**: scus.example.com

## DNS Record Updates

### A Records
```bash
# Update A records for web services
az network dns record-set a add-record \
  --resource-group rg-prod-scus \
  --zone-name scus.example.com \
  --record-set-name www-scus \
  --ipv4-address 10.3.1.10

# Update A records for API endpoints
az network dns record-set a add-record \
  --resource-group rg-prod-scus \
  --zone-name scus.example.com \
  --record-set-name api-scus \
  --ipv4-address 10.3.1.20
```

### CNAME Records
```bash
# Update CNAME for regional services
az network dns record-set cname set-record \
  --resource-group rg-prod-scus \
  --zone-name scus.example.com \
  --record-set-name scus-service \
  --cname scus.internal.example.com
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)