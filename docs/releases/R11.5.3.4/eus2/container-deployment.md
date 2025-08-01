---
ado_organization: '{ vault_eus2_ado_organization }'
azure_region: eastus2
category: agent-upgrade
description: Upgrade monitoring agents across Azure regions
environment: eus2-production
generated_at: '2025-08-01T08:18:32.828919'
region: eus2
tags:
- eus2
- agent-upgrade
- mop
- ansible
- azure-devops
template_source: container-deployment.j2
title: Monitoring Agent Upgrade - EUS2
version: 1.2.0
---


# Container Deployment - EUS2

## Overview

Container deployment procedure for **eastus2** region.

### Container Context

- **Target Region**: EUS2 (eastus2)
- **Container Registry**: acreus2.azurecr.io
- **Image Version**: latest

## Container Deployment

### Pull New Images
```bash
# Login to container registry
ansible eus2_app -m shell -a "
  docker login acreus2.azurecr.io \
  -u  \
  -p 
"

# Pull latest images
ansible eus2_app -m docker_image -a "
  name=acreus2.azurecr.io/webapp:latest
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
  image=acreus2.azurecr.io/webapp:latest
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