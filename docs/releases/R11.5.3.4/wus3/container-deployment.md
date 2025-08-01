---
ado_organization: '{ vault_wus3_ado_organization }'
azure_region: westus3
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: wus3-production
generated_at: '2025-08-01T08:18:32.831870'
region: wus3
tags:
- wus3
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - WUS3
version: 1.2.0
---


# Container Deployment - WUS3

## Overview

Container deployment procedure for **westus3** region.

### Container Context

- **Target Region**: WUS3 (westus3)
- **Container Registry**: acrwus3.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible wus3_app -m shell -a "
  docker login acrwus3.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible wus3_app -m docker_image -a "
  name=acrwus3.azurecr.io/webapp:latest
  source=pull
  force_source=yes
"
```

### Deploy Containers
```bash
# Stop existing containers
ansible wus3_app -m docker_container -a "
  name=webapp
  state=stopped
"

# Start new containers
ansible wus3_app -m docker_container -a "
  name=webapp
  image=acrwus3.azurecr.io/webapp:latest
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
ansible wus3_app -m uri -a "
  url=http://localhost:8080/health
  method=GET
  status_code=200
"
```

---

**Generated**:   
**Template**:   
**Region**: WUS3 (westus3)