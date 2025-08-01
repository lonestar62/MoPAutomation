---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.639763'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: ssl-certificate-renewal.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# SSL Certificate Renewal - WUS3

## Overview

SSL certificate renewal procedure for **westus3** region.

### Certificate Context

- **Target Region**: WUS3 (westus3)
- **Environment**: wus3-production
- **Certificate Authority**: Let's Encrypt / Azure Key Vault
- **Domains**: *.example.com, api.example.com

## Certificate Management

### Certificate Renewal
```bash
# Renew certificates using certbot
ansible wus3_web -m shell -a "certbot renew --dry-run"
ansible wus3_web -m shell -a "certbot renew --force-renewal"

# Deploy certificates to load balancers
ansible wus3_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/fullchain.pem
  dest=/etc/nginx/ssl/
"
ansible wus3_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/privkey.pem
  dest=/etc/nginx/ssl/
"
```

### Service Restart
```bash
# Restart web services to pick up new certificates
ansible wus3_web -m systemd -a "name=nginx state=restarted"
ansible wus3_lb -m systemd -a "name=haproxy state=restarted"
```

### Certificate Validation
```bash
# Verify certificate validity
ansible wus3_web -m uri -a "
  url=https://
  validate_certs=yes
  return_content=no
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)