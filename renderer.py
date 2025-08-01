import os
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, Template
from category_map import CATEGORY_TO_PLAYBOOK
from logger import log_process, mop_logger

class MOPRenderer:
    """Handles MOP template rendering using Jinja2"""
    
    def __init__(self, templates_dir='templates', vars_dir='vars'):
        self.templates_dir = templates_dir
        self.vars_dir = vars_dir
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))
        self.logger = logging.getLogger(__name__)
    
    def list_mops(self):
        """List all available MOPs from variable files"""
        mops = []
        
        if not os.path.exists(self.vars_dir):
            return mops
        
        for filename in os.listdir(self.vars_dir):
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                mop_id = filename.replace('.yml', '').replace('.yaml', '')
                try:
                    variables = self.load_variables(mop_id)
                    if variables:
                        mop_info = {
                            'id': mop_id,
                            'title': variables.get('title', mop_id),
                            'category': variables.get('category', 'unknown'),
                            'region': variables.get('region', 'unknown'),
                            'variables_file': filename
                        }
                        mops.append(mop_info)
                except Exception as e:
                    self.logger.warning(f"Error loading MOP {mop_id}: {e}")
        
        return sorted(mops, key=lambda x: x['id'])
    
    def load_variables(self, mop_id):
        """Load variables from YAML file"""
        var_file = os.path.join(self.vars_dir, f'{mop_id}.yml')
        if not os.path.exists(var_file):
            var_file = os.path.join(self.vars_dir, f'{mop_id}.yaml')
        
        if not os.path.exists(var_file):
            return None
        
        try:
            with open(var_file, 'r') as f:
                variables = yaml.safe_load(f)
                return variables or {}
        except Exception as e:
            self.logger.error(f"Error loading variables from {var_file}: {e}")
            return None
    
    def get_template_for_category(self, category):
        """Get the appropriate template file for a category"""
        # Map categories to template files
        template_map = {
            'patch-linux': 'patch_linux.md.j2',
            'agent-upgrade': 'agent_upgrade.md.j2',
            'pipeline-only': 'pipeline_only.md.j2'
        }
        
        return template_map.get(category, 'patch_linux.md.j2')  # Default template
    
    def render_mop(self, mop_id):
        """Render a MOP using Jinja2 templates"""
        try:
            # Load variables
            variables = self.load_variables(mop_id)
            if not variables:
                raise Exception(f"Variables file not found for MOP {mop_id}")
            
            # Get category and associated playbooks
            category = variables.get('category', 'unknown')
            playbooks = CATEGORY_TO_PLAYBOOK.get(category, [])
            
            # Add playbooks to variables for template rendering
            variables['playbooks'] = playbooks
            
            # Get appropriate template
            template_name = self.get_template_for_category(category)
            
            # Check if template exists
            template_path = os.path.join(self.templates_dir, template_name)
            if not os.path.exists(template_path):
                raise Exception(f"Template {template_name} not found")
            
            # Load and render template
            template = self.jinja_env.get_template(template_name)
            rendered_content = template.render(**variables)
            
            # Parse frontmatter and content
            if rendered_content.startswith('---'):
                parts = rendered_content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_yaml = parts[1].strip()
                    content = parts[2].strip()
                    try:
                        frontmatter = yaml.safe_load(frontmatter_yaml)
                    except:
                        frontmatter = {}
                else:
                    frontmatter = {}
                    content = rendered_content
            else:
                frontmatter = {}
                content = rendered_content
            
            return {
                'id': mop_id,
                'variables': variables,
                'template': template_name,
                'frontmatter': frontmatter,
                'content': content,
                'rendered_content': rendered_content,
                'playbooks': playbooks
            }
            
        except Exception as e:
            self.logger.error(f"Error rendering MOP {mop_id}: {e}")
            raise
    
    def get_template_content(self, template_name):
        """Get raw template content for editing"""
        template_path = os.path.join(self.templates_dir, template_name)
        if not os.path.exists(template_path):
            raise Exception(f"Template {template_name} not found")
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def save_template(self, template_name, content):
        """Save template content"""
        template_path = os.path.join(self.templates_dir, template_name)
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        
        with open(template_path, 'w') as f:
            f.write(content)
    
    def get_variables_content(self, mop_id):
        """Get raw variables content for editing"""
        var_file = os.path.join(self.vars_dir, f'{mop_id}.yml')
        if not os.path.exists(var_file):
            var_file = os.path.join(self.vars_dir, f'{mop_id}.yaml')
        
        if not os.path.exists(var_file):
            # Create a basic template for new MOP
            return f"""id: {mop_id}
title: "New MOP"
category: patch-linux
region: eastus2
# Add your variables here
"""
        
        with open(var_file, 'r') as f:
            return f.read()
    
    def save_variables(self, mop_id, content):
        """Save variables content"""
        var_file = os.path.join(self.vars_dir, f'{mop_id}.yml')
        os.makedirs(os.path.dirname(var_file), exist_ok=True)
        
        with open(var_file, 'w') as f:
            f.write(content)
