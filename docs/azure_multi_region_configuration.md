# Azure Multi-Region Ansible Configuration

## Overview

Our MOP Automation Platform is configured to manage infrastructure across six Azure DevOps regions:

- **eus2** - East US 2 (eastus2)
- **wus2** - West US 2 (westus2)  
- **wus3** - West US 3 (westus3)
- **scus** - South Central US (southcentralus)
- **eus2lea** - East US 2 LEA (eastus2euap)
- **wus2lea** - West US 2 LEA (westus2euap)

## Ansible Inventory Structure

### Regional Inventory Organization
```
inventory/
├── azure_regions.yml              # Main inventory with all regions
├── group_vars/
│   ├── all.yml                    # Global settings
│   ├── eus2.yml                   # East US 2 configuration
│   ├── wus2.yml                   # West US 2 configuration
│   ├── wus3.yml                   # West US 3 configuration
│   ├── scus.yml                   # South Central US configuration
│   ├── eus2lea.yml                # East US 2 LEA configuration
│   └── wus2lea.yml                # West US 2 LEA configuration
└── ansible.cfg                    # Ansible configuration
```

### Host Groups by Region
Each region contains standardized host groups:
- **web_servers**: Load balancers and web applications
- **database_servers**: Database instances
- **monitoring_agents**: Monitoring and observability systems

### Regional Networking
Each region is allocated a /16 network:
- **eus2**: 10.1.0.0/16
- **wus2**: 10.2.0.0/16
- **wus3**: 10.3.0.0/16
- **scus**: 10.4.0.0/16
- **eus2lea**: 10.5.0.0/16
- **wus2lea**: 10.6.0.0/16

## Azure DevOps Integration

### Separate ADO Organizations
Each region has its own complete Azure DevOps organization:
```yaml
ado_organizations:
  eus2:
    organization: "{{ vault_eus2_ado_organization }}"
    project: "{{ vault_eus2_ado_project }}" 
    token: "{{ vault_eus2_ado_token }}"
    pipeline_id: "{{ vault_eus2_pipeline_id }}"
    environment: "{{ vault_eus2_environment }}"
  # ... (repeated for all 6 regions)
```

### Authentication Configuration
- **PAT Tokens**: Separate Personal Access Tokens per ADO organization
- **Service Principals**: Region-specific for Azure resource access
- **Subscriptions**: Separate Azure subscription per region
- **Key Vaults**: Regional key vaults for secrets management
- **Organization Isolation**: Complete separation of ADO organizations

## How Ansible Connects to Azure Regions

### 1. **Dynamic Inventory**
Ansible uses the `azure.azcollection.azure_rm` plugin to discover resources across all six regions automatically.

### 2. **Regional Authentication**
Each region uses dedicated service principals:
```yaml
# Per-region authentication
azure_infrastructure:
  subscription_id: "{{ vault_<region>_subscription_id }}"
  resource_group: "rg-prod-<region>"
  key_vault: "kv-prod-<region>"
```

### 3. **Network Access**
- **Bastion Hosts**: Regional bastion hosts for secure SSH access
- **Private Networks**: All resources on private subnets
- **VPN Connectivity**: Site-to-site VPN for automation server access

### 4. **Playbook Targeting**
Playbooks target specific regions using inventory groups:
```yaml
# Target specific region
hosts: "{{ region }}_{{ target_group | default('web') }}"

# Examples:
# - wus2_web (West US 2 web servers)
# - eus2_monitoring (East US 2 monitoring agents)
# - scus_database (South Central US databases)
```

## MOP Execution Flow for Azure Regions

### 1. **Region Selection**
MOPs specify target region in their variables:
```yaml
# vars/mop-wus2-agent-upgrade-001.yml
region: wus2
```

### 2. **Inventory Resolution**
Ansible resolves region to appropriate host groups:
- `wus2` → targets `wus2_monitoring` hosts
- `eus2` → targets `eus2_monitoring` hosts

### 3. **Pipeline Integration**
Region-specific Azure DevOps pipelines are triggered:
- **eus2** → Pipeline ID from `vault_eus2_pipeline_id`
- **wus2** → Pipeline ID from `vault_wus2_pipeline_id`
- etc.

### 4. **Configuration Management**
Git commits update region-specific configuration files:
- `config/eus2/monitoring-agents.yml`
- `config/wus2/monitoring-agents.yml`
- etc.

## LEA Region Special Handling

### Early Access Regions
**eus2lea** and **wus2lea** are Microsoft Early Access regions with special considerations:

```yaml
# LEA-specific configuration
lea_config:
  early_access: true
  preview_features: true
  canary_deployment: true
```

### Deployment Strategy
- **Maintenance Windows**: Offset by 1 hour from main regions
- **Canary Deployments**: LEA regions receive updates first
- **Preview Features**: Access to pre-release Azure features

## Security and Compliance

### Regional Isolation
- **Network Segregation**: Each region in separate VNets
- **Security Groups**: Region-specific NSG rules
- **Access Control**: RBAC per region and subscription

### Secrets Management
```yaml
# Vault variables per region
vault_eus2_subscription_id: "xxx"
vault_eus2_pipeline_id: "123"
vault_wus2_subscription_id: "yyy"
vault_wus2_pipeline_id: "456"
```

### Compliance
- **Audit Logging**: All actions logged per region
- **Change Tracking**: Git history per regional configuration
- **Approval Gates**: Region-specific approval processes

## Example MOP Execution

### Agent Upgrade Across Regions
```yaml
# MOP targets specific region
id: mop-wus2-agent-upgrade-001
region: wus2

# Ansible execution flow:
1. edit_yaml.yml → Updates config/wus2/monitoring-agents.yml
2. commit_to_git.yml → Commits to wus2 branch
3. run_manual_pipeline.yml → Triggers wus2 deployment pipeline
```

### Multi-Region Deployment
```yaml
# For operations across all regions
category: multi-region-deploy
regions: [eus2, wus2, wus3, scus, eus2lea, wus2lea]

# Sequential execution per region with appropriate targeting
```

This configuration ensures our MOP system can reliably manage infrastructure across all six Azure regions with proper isolation, security, and compliance controls.