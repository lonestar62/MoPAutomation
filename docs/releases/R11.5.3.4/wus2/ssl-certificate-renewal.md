---
ado_organization: '{ vault_wus2_ado_organization }'
azure_region: westus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus2-production
generated_at: '2025-08-01T08:18:32.638330'
region: wus2
tags:
- wus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: ssl-certificate-renewal.j2
title: Monitoring Agent Upgrade - WUS2
version: 1.2.0
---


# SSL Certificate Renewal - WUS2

## Overview

SSL certificate renewal procedure for **westus2** region.

### Certificate Context

- **Target Region**: WUS2 (westus2)
- **Environment**: wus2-production
- **Certificate Authority**: Let's Encrypt / Azure Key Vault
- **Domains**: *.example.com, api.example.com

## Certificate Management

### Certificate Renewal
```bash
# Renew certificates using certbot
ansible wus2_web -m shell -a "certbot renew --dry-run"
ansible wus2_web -m shell -a "certbot renew --force-renewal"

# Deploy certificates to load balancers
ansible wus2_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/fullchain.pem
  dest=/etc/nginx/ssl/
"
ansible wus2_lb -m copy -a "
  src=/etc/letsencrypt/live/example.com/privkey.pem
  dest=/etc/nginx/ssl/
"
```

### Service Restart
```bash
# Restart web services to pick up new certificates
ansible wus2_web -m systemd -a "name=nginx state=restarted"
ansible wus2_lb -m systemd -a "name=haproxy state=restarted"
```

### Certificate Validation
```bash
# Verify certificate validity
ansible wus2_web -m uri -a "
  url=https://
  validate_certs=yes
  return_content=no
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS2 (westus2)