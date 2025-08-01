"""
Category to Playbook mapping configuration
This file defines which Ansible playbooks should be executed for each MOP category
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
    ]
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
