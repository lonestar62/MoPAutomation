---
ado_organization: '{ vault_scus_ado_organization }'
azure_region: southcentralus
category: general
description: MOP documentation for scus
environment: scus-production
generated_at: '2025-08-01T08:26:36.754311'
region: scus
tags:
- scus
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - SCUS
version: '1.0'
---


# Container Deployment - SCUS

## Overview

Container deployment procedure for **southcentralus** region.

### Container Context

- **Target Region**: SCUS (southcentralus)
- **Container Registry**: acrscusprod.azurecr.io
- **Image Version**: 1.2.0

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible scus_app -m shell -a "
  docker login acrscusprod.azurecr.io \
  -u {{ vault_scus_acr_username }} \
  -p {{ vault_scus_acr_password }}
"

# Pull latest images
ansible scus_app -m docker_image -a "
  name=acrscusprod.azurecr.io/webapp:1.2.0
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible scus_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible scus_app -m docker_container -a "
  name=webapp
  image=acrscusprod.azurecr.io/webapp:1.2.0
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_scus_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_scus_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible scus_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: SCUS (southcentralus)