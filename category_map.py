"""
Category to Playbook mapping configuration for Azure multi-region deployment
This file defines which Ansible playbooks should be executed for each MOP category
across our six Azure regions: eus2, wus2, wus3, scus, eus2lea, wus2lea
"""

CATEGORY_TO_PLAYBOOK = {
    "patch-linux": [
        "patch_linux.yml"
    ],
    "agent-upgrade": [
        "edit_yaml.yml",
        "commit_to_git.yml", 
        "run_manual_pipeline.yml"
    ],
    "pipeline-only": [
        "run_manual_pipeline.yml"
    ],
    "git-ops": [
        "edit_yaml.yml",
        "commit_to_git.yml"
    ],
    "infrastructure": [
        "edit_yaml.yml",
        "commit_to_git.yml",
        "run_manual_pipeline.yml"
    ],
    "multi-region-patch": [
        "patch_linux.yml"  # Will target all regions based on inventory
    ],
    "multi-region-deploy": [
        "edit_yaml.yml",
        "commit_to_git.yml",
        "run_manual_pipeline.yml"  # Will deploy to specific region
    ]
}

# Azure region mappings
AZURE_REGIONS = {
    "eus2": {
        "name": "East US 2",
        "azure_name": "eastus2",
        "timezone": "America/New_York"
    },
    "wus2": {
        "name": "West US 2", 
        "azure_name": "westus2",
        "timezone": "America/Los_Angeles"
    },
    "wus3": {
        "name": "West US 3",
        "azure_name": "westus3", 
        "timezone": "America/Los_Angeles"
    },
    "scus": {
        "name": "South Central US",
        "azure_name": "southcentralus",
        "timezone": "America/Chicago"
    },
    "eus2lea": {
        "name": "East US 2 LEA",
        "azure_name": "eastus2euap",
        "timezone": "America/New_York"
    },
    "wus2lea": {
        "name": "West US 2 LEA", 
        "azure_name": "westus2euap",
        "timezone": "America/Los_Angeles"
    }
}

def get_playbooks_for_category(category):
    """Get list of playbooks for a given category"""
    return CATEGORY_TO_PLAYBOOK.get(category, [])

def get_all_categories():
    """Get all available categories"""
    return list(CATEGORY_TO_PLAYBOOK.keys())

def validate_category(category):
    """Check if a category is valid"""
    return category in CATEGORY_TO_PLAYBOOK
