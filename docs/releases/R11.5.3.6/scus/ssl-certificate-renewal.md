---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:27:10.719119'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: ssl-certificate-renewal.j2
title: ssl-certificate-renewal.j2 - SCUS
version: '1.0'
---


# SSL Certificate Renewal - SCUS

## Overview

SSL certificate renewal procedure for **southcentralus** region.

### Certificate Context

- **Target Region**: SCUS (southcentralus)
- **Environment**: scus-production
- **Certificate Authority**: Let's Encrypt / Azure Key Vault
- **Domains**: *.scus.example.com, api-scus.example.com, app-scus.example.com

## Certificate Management

### Certificate Renewal
```bash
# Renew certificates using certbot
ansible scus_web -m shell -a "certbot renew --dry-run"
ansible scus_web -m shell -a "certbot renew --force-renewal"

# Deploy certificates to load balancers
ansible scus_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/fullchain.pem
  dest=/etc/nginx/ssl/
"
ansible scus_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/privkey.pem
  dest=/etc/nginx/ssl/
"
```

### Service Restart
```bash
# Restart web services to pick up new certificates
ansible scus_web -m systemd -a "name=nginx state=restarted"
ansible scus_lb -m systemd -a "name=haproxy state=restarted"
```

### Certificate Validation
```bash
# Verify certificate validity
ansible scus_web -m uri -a "
  url=https://
  validate_certs=yes
  return_content=no
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)