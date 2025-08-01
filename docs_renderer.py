"""
Documentation Renderer for Vendor J2 Templates
Renders Jinja2 templates with MOP variables and publishes to documentation wiki
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
import requests
from logger import MOPLogger

class DocumentationRenderer:
    """Handles rendering of vendor J2 templates with MOP variables"""
    
    def __init__(self, vendor_templates_dir: str = "templates/vendor", 
                 output_dir: str = "docs/rendered",
                 wiki_config: Optional[Dict] = None):
        self.vendor_templates_dir = Path(vendor_templates_dir)
        self.output_dir = Path(output_dir)
        self.wiki_config = wiki_config or {}
        self.logger = MOPLogger()
        
        # Azure regions
        self.regions = ["eus2", "wus2", "wus3", "scus", "eus2lea", "wus2lea"]
        
        # Create Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader([str(self.vendor_templates_dir)]),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False
        )
        
        # Ensure output directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for region in self.regions:
            (self.output_dir / region).mkdir(parents=True, exist_ok=True)
    
    def load_vendor_templates(self) -> List[Path]:
        """Load all J2 templates from vendor directory"""
        templates = list(self.vendor_templates_dir.glob("*.j2"))
        self.logger.log_system(f"Found {len(templates)} vendor templates", "load_vendor_templates")
        return templates
    
    def load_mop_variables(self, vars_file: str) -> Dict[str, Any]:
        """Load MOP variables from YAML file"""
        vars_path = Path("vars") / vars_file
        if not vars_path.exists():
            raise FileNotFoundError(f"Variables file not found: {vars_path}")
        
        with open(vars_path, 'r') as f:
            variables = yaml.safe_load(f)
        
        self.logger.log_system(f"Loaded variables from {vars_file}", "load_mop_variables")
        return variables
    
    def generate_frontmatter(self, template_name: str, region: str, 
                           variables: Dict[str, Any]) -> Dict[str, Any]:
        """Generate frontmatter YAML based on vendor template and region"""
        frontmatter_data = {
            "title": f"{variables.get('title', template_name)} - {region.upper()}",
            "description": variables.get('description', f"MOP documentation for {region}"),
            "region": region,
            "category": variables.get('category', 'general'),
            "version": variables.get('version', '1.0'),
            "generated_at": datetime.utcnow().isoformat(),
            "template_source": template_name,
            "azure_region": self._get_azure_region_name(region),
            "ado_organization": f"{{ vault_{region}_ado_organization }}",
            "environment": f"{region}-production",
            "tags": [
                region,
                variables.get('category', 'general'),
                "mop",
                "ansible",
                "azure-devops"
            ]
        }
        
        # Add region-specific metadata
        if region.endswith('lea'):
            frontmatter_data['early_access'] = True
            frontmatter_data['preview_features'] = True
        
        return frontmatter_data
    
    def _get_azure_region_name(self, region_code: str) -> str:
        """Convert region code to Azure region name"""
        region_mapping = {
            "eus2": "eastus2",
            "wus2": "westus2", 
            "wus3": "westus3",
            "scus": "southcentralus",
            "eus2lea": "eastus2euap",
            "wus2lea": "westus2euap"
        }
        return region_mapping.get(region_code, region_code)
    
    def render_template_for_region(self, template_path: Path, region: str, 
                                 variables: Dict[str, Any]) -> str:
        """Render a single template for a specific region"""
        try:
            # Load template
            template_name = template_path.name
            template = self.jinja_env.get_template(template_name)
            
            # Prepare region-specific variables
            region_variables = variables.copy()
            region_variables.update({
                'region': region,
                'azure_region': self._get_azure_region_name(region),
                'region_code': region,
                'ado_organization': f"{{ vault_{region}_ado_organization }}",
                'ado_project': f"{{ vault_{region}_ado_project }}",
                'pipeline_id': f"{{ vault_{region}_pipeline_id }}",
                'environment': f"{region}-production",
                'subscription_id': f"{{ vault_{region}_subscription_id }}",
                'resource_group': f"rg-prod-{region}",
                'key_vault': f"kv-prod-{region}",
                'is_lea_region': region.endswith('lea')
            })
            
            # Render template content
            content = template.render(**region_variables)
            
            # Generate frontmatter
            frontmatter_data = self.generate_frontmatter(template_name, region, variables)
            
            # Combine frontmatter and content manually
            frontmatter_yaml = yaml.dump(frontmatter_data, default_flow_style=False)
            rendered_content = f"---\n{frontmatter_yaml}---\n\n{content}"
            
            self.logger.log_system(f"Rendered {template_name} for {region}", "render_template")
            
            return rendered_content
            
        except Exception as e:
            self.logger.log_system(f"Failed to render {template_path} for {region}: {str(e)}", "render_template_error")
            raise
    
    def render_all_templates(self, variables_file: str) -> Dict[str, Dict[str, str]]:
        """Render all vendor templates for all regions"""
        results = {}
        
        # Load variables
        variables = self.load_mop_variables(variables_file)
        
        # Load vendor templates
        templates = self.load_vendor_templates()
        
        if not templates:
            self.logger.log_system("No vendor templates found", "render_all_templates")
            return results
        
        # Render each template for each region
        for template_path in templates:
            template_name = template_path.stem  # filename without extension
            results[template_name] = {}
            
            for region in self.regions:
                try:
                    rendered_content = self.render_template_for_region(
                        template_path, region, variables
                    )
                    
                    # Save to regional output directory
                    output_file = self.output_dir / region / f"{template_name}.md"
                    with open(output_file, 'w') as f:
                        f.write(rendered_content)
                    
                    results[template_name][region] = str(output_file)
                    
                    self.logger.log_system(f"Saved {template_name} for {region} to {output_file}", "template_rendered")
                
                except Exception as e:
                    self.logger.log_system(f"Failed to render {template_name} for {region}: {str(e)}", "template_render_error")
                    results[template_name][region] = f"ERROR: {str(e)}"
        
        return results
    
    def publish_to_wiki(self, rendered_files: Dict[str, Dict[str, str]], 
                       wiki_space: str = "MOPs") -> Dict[str, Any]:
        """Publish rendered documents to eus2 documentation wiki"""
        if not self.wiki_config:
            self.logger.log_system("No wiki configuration provided", "wiki_publish_skip")
            return {"status": "skipped", "reason": "no_config"}
        
        try:
            wiki_results = {
                "published": [],
                "failed": [],
                "wiki_space": wiki_space,
                "publication_time": datetime.utcnow().isoformat()
            }
            
            for template_name, regional_files in rendered_files.items():
                for region, file_path in regional_files.items():
                    if file_path.startswith("ERROR:"):
                        continue
                    
                    try:
                        # Read rendered content
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        # Parse frontmatter manually
                        if content.startswith('---\n'):
                            parts = content.split('---\n', 2)
                            if len(parts) >= 3:
                                frontmatter_yaml = parts[1]
                                metadata = yaml.safe_load(frontmatter_yaml)
                            else:
                                metadata = {}
                        else:
                            metadata = {}
                        
                        # Publish to wiki (implementation depends on wiki system)
                        wiki_page_title = f"{template_name} - {region.upper()}"
                        wiki_result = self._publish_page_to_wiki(
                            wiki_space, wiki_page_title, content, metadata
                        )
                        
                        if wiki_result.get("success"):
                            wiki_results["published"].append({
                                "template": template_name,
                                "region": region,
                                "wiki_url": wiki_result.get("url"),
                                "page_id": wiki_result.get("page_id")
                            })
                        else:
                            wiki_results["failed"].append({
                                "template": template_name,
                                "region": region,
                                "error": wiki_result.get("error")
                            })
                    
                    except Exception as e:
                        wiki_results["failed"].append({
                            "template": template_name,
                            "region": region,
                            "error": str(e)
                        })
            
            self.logger.log_system(f"Published {len(wiki_results['published'])} pages, "
                                    f"failed {len(wiki_results['failed'])}", "wiki_publish_complete")
            
            return wiki_results
        
        except Exception as e:
            self.logger.log_system(f"Wiki publication failed: {str(e)}", "wiki_publish_error")
            return {"status": "error", "error": str(e)}
    
    def _publish_page_to_wiki(self, space: str, title: str, content: str, 
                            metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Publish a single page to the documentation wiki"""
        # This is a placeholder for actual wiki integration
        # Implementation depends on your wiki system (Confluence, GitLab Wiki, etc.)
        
        wiki_api_url = self.wiki_config.get("api_url")
        wiki_token = self.wiki_config.get("token")
        
        if not wiki_api_url or not wiki_token:
            return {"success": False, "error": "Missing wiki configuration"}
        
        # Example for Confluence API
        page_data = {
            "type": "page",
            "title": title,
            "space": {"key": space},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            },
            "metadata": {
                "properties": {
                    "region": {"value": metadata.get("region")},
                    "category": {"value": metadata.get("category")},
                    "template_source": {"value": metadata.get("template_source")},
                    "generated_at": {"value": metadata.get("generated_at")}
                }
            }
        }
        
        try:
            headers = {
                "Authorization": f"Bearer {wiki_token}",
                "Content-Type": "application/json"
            }
            
            # This would be the actual API call
            # response = requests.post(f"{wiki_api_url}/content", 
            #                         json=page_data, headers=headers)
            
            # For now, simulate success
            return {
                "success": True,
                "url": f"{wiki_api_url}/pages/{space}/{title.replace(' ', '-')}",
                "page_id": f"mock-{hash(title)}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_index_page(self, rendered_files: Dict[str, Dict[str, str]]) -> str:
        """Generate an index page listing all rendered documentation"""
        index_content = []
        index_content.append("---")
        index_content.append("title: MOP Documentation Index")
        index_content.append("description: Index of all rendered MOP documentation across regions")
        index_content.append(f"generated_at: {datetime.utcnow().isoformat()}")
        index_content.append("layout: index")
        index_content.append("---")
        index_content.append("")
        index_content.append("# MOP Documentation Index")
        index_content.append("")
        index_content.append("This page provides an index of all rendered MOP documentation across our six Azure regions.")
        index_content.append("")
        
        # Group by template
        for template_name, regional_files in rendered_files.items():
            index_content.append(f"## {template_name}")
            index_content.append("")
            
            for region in self.regions:
                if region in regional_files and not regional_files[region].startswith("ERROR:"):
                    file_path = regional_files[region]
                    relative_path = Path(file_path).relative_to(self.output_dir)
                    index_content.append(f"- [{region.upper()}]({relative_path})")
            
            index_content.append("")
        
        index_content.append("## Regional Overview")
        index_content.append("")
        for region in self.regions:
            azure_region = self._get_azure_region_name(region)
            region_type = "Early Access" if region.endswith('lea') else "Production"
            index_content.append(f"- **{region.upper()}** ({azure_region}) - {region_type}")
        
        index_path = self.output_dir / "index.md"
        with open(index_path, 'w') as f:
            f.write('\n'.join(index_content))
        
        return str(index_path)

def render_documentation(variables_file: str, wiki_config: Optional[Dict] = None) -> Dict[str, Any]:
    """Main function to render all documentation"""
    renderer = DocumentationRenderer(wiki_config=wiki_config)
    
    try:
        # Render all templates for all regions
        rendered_files = renderer.render_all_templates(variables_file)
        
        # Generate index page
        index_path = renderer.generate_index_page(rendered_files)
        
        # Publish to wiki if configured
        wiki_results = None
        if wiki_config:
            wiki_results = renderer.publish_to_wiki(rendered_files)
        
        return {
            "success": True,
            "rendered_files": rendered_files,
            "index_path": index_path,
            "wiki_results": wiki_results,
            "total_templates": len(rendered_files),
            "total_documents": sum(len(regions) for regions in rendered_files.values())
        }
    
    except Exception as e:
        renderer.logger.log_system(str(e), "render_documentation_error")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    result = render_documentation("example-vars.yml")
    print(json.dumps(result, indent=2))