---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: general
description: MOP documentation for eus2lea
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:26:36.766621'
preview_features: true
region: eus2lea
tags:
- eus2lea
- general
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: container-deployment.j2 - EUS2LEA
version: '1.0'
---


# Container Deployment - EUS2LEA

## Overview

Container deployment procedure for **eastus2euap** region.

### Container Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Container Registry**: acreus2leaprod.azurecr.io
- **Image Version**: 1.3.0-preview

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible eus2lea_app -m shell -a "
  docker login acreus2leaprod.azurecr.io \
  -u {{ vault_eus2lea_acr_username }} \
  -p {{ vault_eus2lea_acr_password }}
"

# Pull latest images
ansible eus2lea_app -m docker_image -a "
  name=acreus2leaprod.azurecr.io/webapp:1.3.0-preview
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible eus2lea_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible eus2lea_app -m docker_container -a "
  name=webapp
  image=acreus2leaprod.azurecr.io/webapp:1.3.0-preview
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=mysql://appuser:{{ vault_eus2lea_db_password }}@{{ db_ip }}:3306/ProductionDB
    API_KEY={{ vault_eus2lea_api_key }}
"
```

### Health Validation
```bash
# Check container health
ansible eus2lea_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: EUS2LEA (eastus2euap)