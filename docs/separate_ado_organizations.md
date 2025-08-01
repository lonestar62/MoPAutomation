# Separate Azure DevOps Organizations Configuration

## Architecture Overview

Our MOP Automation Platform is configured to work with **six separate Azure DevOps organizations**, each managing their own region:

```
Region → ADO Organization → Pipelines & Environments
├── eus2 → Organization A → eus2-production environment
├── wus2 → Organization B → wus2-production environment  
├── wus3 → Organization C → wus3-production environment
├── scus → Organization D → scus-production environment
├── eus2lea → Organization E → eus2lea-production environment
└── wus2lea → Organization F → wus2lea-production environment
```

## Per-Organization Configuration

### Vault Variables Required

Each ADO organization requires its own set of authentication credentials:

```yaml
# East US 2 Organization
vault_eus2_ado_organization: "mycompany-eus2"
vault_eus2_ado_project: "infrastructure"
vault_eus2_ado_token: "pat_token_for_eus2_org"
vault_eus2_pipeline_id: "123"
vault_eus2_environment: "eus2-production"

# West US 2 Organization  
vault_wus2_ado_organization: "mycompany-wus2"
vault_wus2_ado_project: "infrastructure"
vault_wus2_ado_token: "pat_token_for_wus2_org" 
vault_wus2_pipeline_id: "456"
vault_wus2_environment: "wus2-production"

# ... (similar for wus3, scus, eus2lea, wus2lea)
```

### Regional ADO Organization Mapping

```yaml
# inventory/group_vars/all.yml
ado_organizations:
  eus2:
    organization: "{{ vault_eus2_ado_organization }}"
    project: "{{ vault_eus2_ado_project }}"
    token: "{{ vault_eus2_ado_token }}"
    base_url: "https://dev.azure.com/{{ vault_eus2_ado_organization }}"
    pipeline_id: "{{ vault_eus2_pipeline_id }}"
    environment: "{{ vault_eus2_environment }}"
  # ... (repeated for all 6 regions)
```

## How Pipeline Execution Works

### 1. MOP Specifies Target Region
```yaml
# vars/mop-eus2-agent-upgrade-001.yml
region: eus2
target_group: monitoring
```

### 2. Ansible Resolves ADO Organization
```yaml
# Playbook automatically resolves:
current_region: "eus2"
region_ado_config: "{{ ado_organizations['eus2'] }}"

# Results in:
devops_organization: "mycompany-eus2"  
devops_project: "infrastructure"
pipeline_id: "123"
azure_devops_token: "pat_token_for_eus2_org"
base_url: "https://dev.azure.com/mycompany-eus2"
```

### 3. API Call to Correct Organization
```yaml
# API endpoint becomes region-specific:
url: "https://dev.azure.com/mycompany-eus2/infrastructure/_apis/pipelines/123/runs"
headers:
  Authorization: "Basic {{ ('':pat_token_for_eus2_org) | b64encode }}"
```

## Example Real-World Scenario

### Corporate Structure
```
Company XYZ has 6 separate ADO organizations:

├── xyz-eastus2 (eus2)
│   ├── Project: DataCenter-Operations
│   ├── Pipeline ID: 789
│   └── Environment: eus2-production
│
├── xyz-westus2 (wus2)  
│   ├── Project: CloudInfra-West
│   ├── Pipeline ID: 456
│   └── Environment: wus2-production
│
├── xyz-westus3 (wus3)
│   ├── Project: ModernApps-West3
│   ├── Pipeline ID: 123
│   └── Environment: wus3-production
│
└── ... (etc for scus, eus2lea, wus2lea)
```

### MOP Execution Flow

1. **Agent Upgrade for East US 2**:
   ```yaml
   # MOP: mop-eus2-agent-upgrade-001.yml
   region: eus2
   
   # Resolves to:
   organization: "xyz-eastus2"
   project: "DataCenter-Operations" 
   pipeline: 789
   token: "eus2_specific_pat_token"
   ```

2. **Infrastructure Deployment for West US 3**:
   ```yaml
   # MOP: mop-wus3-infrastructure-002.yml  
   region: wus3
   
   # Resolves to:
   organization: "xyz-westus3"
   project: "ModernApps-West3"
   pipeline: 123
   token: "wus3_specific_pat_token"
   ```

## Authentication & Security

### Separate PAT Tokens
Each organization requires its own Personal Access Token:
- **eus2**: PAT with permissions to `xyz-eastus2` organization only
- **wus2**: PAT with permissions to `xyz-westus2` organization only  
- **wus3**: PAT with permissions to `xyz-westus3` organization only
- etc.

### Organization Isolation
- **Network**: Each ADO org can have different network restrictions
- **Permissions**: Users may have access to only specific organizations
- **Compliance**: Different compliance requirements per region/organization
- **Billing**: Separate billing and cost allocation per organization

## Configuration Validation

### Ansible Validation Checks
```yaml
- name: Validate region and ADO organization configuration
  assert:
    that:
      - current_region in ado_organizations
      - region_ado_config is defined
      - region_ado_config.organization is defined
      - region_ado_config.project is defined  
      - region_ado_config.pipeline_id is defined
      - region_ado_config.token is defined
    fail_msg: "Region {{ current_region }} ADO organization not configured"
```

### Error Handling
- **Missing Organization**: Fails if region not configured
- **Invalid Credentials**: Handles authentication failures per organization
- **Pipeline Not Found**: Regional pipeline lookup validation
- **Environment Issues**: Environment-specific deployment failures

## Benefits of Separate Organizations

### 1. **Regional Autonomy**
- Each region team manages their own ADO organization
- Independent project structures and naming conventions
- Regional compliance and governance policies

### 2. **Security Isolation**  
- Blast radius containment per region
- Separate authentication boundaries
- Region-specific access controls

### 3. **Operational Independence**
- No cross-region dependencies for deployments
- Independent maintenance windows and processes
- Region-specific tooling and extensions

### 4. **Billing & Cost Management**
- Clear cost allocation per region
- Separate budgets and billing accounts
- Regional resource tracking

## Multi-Region Deployment Example

```yaml
# For operations across multiple organizations:
- name: Deploy to multiple regions
  include_tasks: run_manual_pipeline.yml
  vars:
    region: "{{ item }}"
  loop:
    - eus2    # → xyz-eastus2 organization
    - wus2    # → xyz-westus2 organization  
    - wus3    # → xyz-westus3 organization
    - scus    # → xyz-southcentral organization
    - eus2lea # → xyz-eastus2-lea organization
    - wus2lea # → xyz-westus2-lea organization
```

Each iteration connects to a completely separate Azure DevOps organization with its own authentication, projects, pipelines, and environments.

This architecture ensures our MOP automation can operate across your distributed organizational structure while maintaining proper isolation and security boundaries.