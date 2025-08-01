---
ado_organization: '{ vault_eus2lea_ado_organization }'
azure_region: eastus2euap
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
early_access: true
environment: eus2lea-production
generated_at: '2025-08-01T08:18:32.834603'
preview_features: true
region: eus2lea
tags:
- eus2lea
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - EUS2LEA
version: 1.2.0
---


# Container Deployment - EUS2LEA

## Overview

Container deployment procedure for **eastus2euap** region.

### Container Context

- **Target Region**: EUS2LEA (eastus2euap)
- **Container Registry**: acreus2lea.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible eus2lea_app -m shell -a "
  docker login acreus2lea.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible eus2lea_app -m docker_image -a "
  name=acreus2lea.azurecr.io/webapp:latest
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
  image=acreus2lea.azurecr.io/webapp:latest
  state=started
  restart_policy=always
  ports=8080:80
  env:
    DATABASE_URL=
    API_KEY=
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