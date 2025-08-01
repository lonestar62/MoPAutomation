---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: general
description: MOP documentation for eus2
environment: eus2-production
generated_at: '2025-08-01T08:26:36.720060'
region: eus2
tags:
- eus2
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - EUS2
version: '1.0'
---


# Container Deployment - EUS2

## Overview

Container deployment procedure for **eastus2** region.

### Container Context

- **Target Region**: EUS2 (eastus2)
- **Container Registry**: acreus2prod.azurecr.io
- **Image Version**: 1.2.0

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible eus2_app -m shell -a "
  docker login acreus2prod.azurecr.io \
  -u {{ vault_eus2_acr_username }} \
  -p {{ vault_eus2_acr_password }}
"

# Pull latest images
ansible eus2_app -m docker_image -a "
  name=acreus2prod.azurecr.io/webapp:1.2.0
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible eus2_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible eus2_app -m docker_container -a "
  name=webapp
  image=acreus2prod.azurecr.io/webapp:1.2.0
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_eus2_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_eus2_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible eus2_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2 (eastus2)