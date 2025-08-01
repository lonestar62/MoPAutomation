"""
MOP Release Management System
Handles vendor MOP processing, type detection, and sequential execution across Azure organizations
"""

import os
import yaml
import json
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from jinja2 import Environment, FileSystemLoader

from logger import MOPLogger
from docs_renderer import DocumentationRenderer
from category_map import CATEGORY_TO_PLAYBOOK

class MOPType(Enum):
    """MOP types that map to specific Ansible playbooks"""
    AGENT_UPGRADE = "agent-upgrade"
    INFRASTRUCTURE = "infrastructure"
    PATCH_LINUX = "patch-linux"
    PIPELINE_ONLY = "pipeline-only"
    GIT_OPS = "git-ops"
    NETWORK = "network"
    SECURITY = "security"
    DATABASE = "database"
    MONITORING = "monitoring"
    BACKUP = "backup"

class ExecutionStatus(Enum):
    """Execution status for MOPs and regions"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"

@dataclass
class MOPDefinition:
    """Definition of a single MOP"""
    id: str
    name: str
    description: str
    mop_type: MOPType
    template_path: str
    variables_required: List[str]
    playbooks: List[str]
    estimated_duration: int  # minutes
    dependencies: List[str]  # other MOP IDs
    risk_level: str  # low, medium, high
    approval_required: bool

@dataclass
class RegionExecution:
    """Execution status for a specific region"""
    region: str
    status: ExecutionStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    artifacts: List[str] = None

@dataclass
class MOPExecution:
    """Execution tracking for a single MOP across all regions"""
    mop_id: str
    release_version: str
    status: ExecutionStatus
    regions: Dict[str, RegionExecution]
    created_at: str
    updated_at: str

@dataclass
class ReleaseDefinition:
    """Complete release with all MOPs"""
    version: str
    description: str
    created_at: str
    created_by: str
    mops: List[MOPDefinition]
    execution_order: List[str]  # region execution order
    status: ExecutionStatus
    current_region: Optional[str] = None
    current_mop: Optional[str] = None

class MOPReleaseManager:
    """Manages MOP releases, type detection, and sequential execution"""
    
    def __init__(self, base_docs_path: str = "docs", releases_path: str = "releases"):
        self.base_docs_path = Path(base_docs_path)
        self.releases_path = Path(releases_path)
        self.vendor_templates_path = Path("templates/vendor")
        self.logger = MOPLogger()
        
        # Standard execution order for Azure organizations
        self.execution_order = ["eus2", "wus2", "wus3", "scus", "eus2lea", "wus2lea"]
        
        # Ensure directories exist
        self.releases_path.mkdir(exist_ok=True)
        (self.releases_path / "configs").mkdir(exist_ok=True)
        (self.releases_path / "executions").mkdir(exist_ok=True)
        
        # MOP type detection patterns
        self.type_patterns = {
            MOPType.AGENT_UPGRADE: [
                r"agent.*upgrade", r"monitoring.*agent", r"upgrade.*agent",
                r"agent.*update", r"collector.*upgrade"
            ],
            MOPType.INFRASTRUCTURE: [
                r"infrastructure.*deploy", r"deploy.*infrastructure", r"infra.*provision",
                r"resource.*provision", r"azure.*deploy", r"cloud.*deploy"
            ],
            MOPType.PATCH_LINUX: [
                r"patch.*linux", r"linux.*patch", r"os.*patch", r"system.*patch",
                r"update.*linux", r"linux.*update"
            ],
            MOPType.PIPELINE_ONLY: [
                r"pipeline.*only", r"ado.*pipeline", r"devops.*pipeline",
                r"ci.*cd", r"build.*deploy"
            ],
            MOPType.GIT_OPS: [
                r"git.*ops", r"gitops", r"repository.*sync", r"git.*deploy",
                r"source.*control"
            ],
            MOPType.NETWORK: [
                r"network.*config", r"firewall.*config", r"dns.*config",
                r"load.*balancer", r"network.*security"
            ],
            MOPType.SECURITY: [
                r"security.*config", r"certificate.*deploy", r"ssl.*config",
                r"security.*patch", r"vulnerability.*fix"
            ],
            MOPType.DATABASE: [
                r"database.*config", r"db.*deploy", r"sql.*config",
                r"database.*patch", r"db.*maintenance"
            ],
            MOPType.MONITORING: [
                r"monitoring.*config", r"alerting.*config", r"dashboard.*deploy",
                r"metrics.*config", r"logging.*config"
            ],
            MOPType.BACKUP: [
                r"backup.*config", r"restore.*procedure", r"disaster.*recovery",
                r"backup.*verification", r"data.*protection"
            ]
        }
    
    def detect_mop_type(self, template_content: str, template_name: str) -> MOPType:
        """Detect MOP type from template content and name"""
        content_lower = template_content.lower()
        name_lower = template_name.lower()
        
        # Check template name first
        for mop_type, patterns in self.type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower) or re.search(pattern, content_lower):
                    self.logger.log_system(f"Detected MOP type {mop_type.value} for {template_name}", "mop_type_detection")
                    return mop_type
        
        # Default to infrastructure if no match
        self.logger.log_system(f"No specific type detected for {template_name}, defaulting to infrastructure", "mop_type_detection")
        return MOPType.INFRASTRUCTURE
    
    def extract_mop_metadata(self, template_path: Path) -> Dict[str, Any]:
        """Extract metadata from MOP template"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Look for YAML frontmatter or special comments
            metadata = {
                'id': template_path.stem,
                'name': template_path.stem.replace('-', ' ').title(),
                'description': f"MOP procedure: {template_path.stem}",
                'estimated_duration': 30,  # default 30 minutes
                'risk_level': 'medium',
                'approval_required': True,
                'dependencies': [],
                'variables_required': []
            }
            
            # Extract variables from template
            jinja_vars = re.findall(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)', content)
            metadata['variables_required'] = list(set(jinja_vars))
            
            # Look for metadata comments
            metadata_match = re.search(r'{#\s*METADATA:(.*?)#}', content, re.DOTALL)
            if metadata_match:
                try:
                    metadata_yaml = yaml.safe_load(metadata_match.group(1))
                    metadata.update(metadata_yaml)
                except yaml.YAMLError:
                    pass
            
            return metadata
        
        except Exception as e:
            self.logger.log_system(f"Error extracting metadata from {template_path}: {e}", "metadata_extraction", "error")
            return {}
    
    def get_playbooks_for_type(self, mop_type: MOPType) -> List[str]:
        """Get Ansible playbooks for a specific MOP type"""
        # Map MOP types to category strings used in CATEGORY_TO_PLAYBOOK
        type_to_category = {
            MOPType.AGENT_UPGRADE: "agent-upgrade",
            MOPType.INFRASTRUCTURE: "infrastructure",
            MOPType.PATCH_LINUX: "patch-linux",
            MOPType.PIPELINE_ONLY: "pipeline-only",
            MOPType.GIT_OPS: "git-ops",
            MOPType.NETWORK: "infrastructure",  # Use infrastructure playbooks
            MOPType.SECURITY: "infrastructure",
            MOPType.DATABASE: "infrastructure",
            MOPType.MONITORING: "agent-upgrade",  # Similar to agent upgrade
            MOPType.BACKUP: "infrastructure"
        }
        
        category = type_to_category.get(mop_type, "infrastructure")
        playbooks = CATEGORY_TO_PLAYBOOK.get(category, ["run_manual_pipeline.yml"])
        
        return playbooks if isinstance(playbooks, list) else [playbooks]
    
    def process_vendor_mops(self, vendor_templates_dir: str, release_version: str, 
                           description: str = "", created_by: str = "system") -> ReleaseDefinition:
        """Process all vendor MOPs and create a release definition"""
        self.logger.log_system(f"Processing vendor MOPs for release {release_version}", "process_vendor_mops")
        
        vendor_path = Path(vendor_templates_dir)
        if not vendor_path.exists():
            raise FileNotFoundError(f"Vendor templates directory not found: {vendor_templates_dir}")
        
        mops = []
        j2_files = list(vendor_path.glob("*.j2"))
        
        if not j2_files:
            raise ValueError(f"No J2 templates found in {vendor_templates_dir}")
        
        for template_path in j2_files:
            try:
                # Read template content
                with open(template_path, 'r') as f:
                    content = f.read()
                
                # Detect MOP type
                mop_type = self.detect_mop_type(content, template_path.name)
                
                # Extract metadata
                metadata = self.extract_mop_metadata(template_path)
                
                # Get associated playbooks
                playbooks = self.get_playbooks_for_type(mop_type)
                
                # Create MOP definition
                mop = MOPDefinition(
                    id=metadata.get('id', template_path.stem),
                    name=metadata.get('name', template_path.stem.replace('-', ' ').title()),
                    description=metadata.get('description', f"MOP procedure: {template_path.stem}"),
                    mop_type=mop_type,
                    template_path=str(template_path),
                    variables_required=metadata.get('variables_required', []),
                    playbooks=playbooks,
                    estimated_duration=metadata.get('estimated_duration', 30),
                    dependencies=metadata.get('dependencies', []),
                    risk_level=metadata.get('risk_level', 'medium'),
                    approval_required=metadata.get('approval_required', True)
                )
                
                mops.append(mop)
                self.logger.log_system(f"Processed MOP {mop.id} ({mop_type.value})", "mop_processed")
            
            except Exception as e:
                self.logger.log_system(f"Error processing template {template_path}: {e}", "mop_processing_error", "error")
                continue
        
        # Create release definition
        release = ReleaseDefinition(
            version=release_version,
            description=description or f"Release {release_version} with {len(mops)} MOPs",
            created_at=datetime.utcnow().isoformat(),
            created_by=created_by,
            mops=mops,
            execution_order=self.execution_order.copy(),
            status=ExecutionStatus.PENDING
        )
        
        # Save release definition
        self.save_release_definition(release)
        
        self.logger.log_system(f"Created release {release_version} with {len(mops)} MOPs", "release_created")
        return release
    
    def save_release_definition(self, release: ReleaseDefinition):
        """Save release definition to file"""
        config_path = self.releases_path / "configs" / f"{release.version}.json"
        
        # Convert to dict with proper enum serialization
        release_dict = asdict(release)
        release_dict['status'] = release.status.value
        
        # Convert MOPs enum values
        for mop in release_dict['mops']:
            mop['mop_type'] = mop['mop_type'].value if hasattr(mop['mop_type'], 'value') else mop['mop_type']
        
        with open(config_path, 'w') as f:
            json.dump(release_dict, f, indent=2, default=str)
    
    def load_release_definition(self, release_version: str) -> ReleaseDefinition:
        """Load release definition from file"""
        config_path = self.releases_path / "configs" / f"{release_version}.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Release {release_version} not found")
        
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        # Convert dictionaries back to dataclass instances
        if isinstance(data['status'], str):
            data['status'] = ExecutionStatus(data['status'])
        data['execution_order'] = data['execution_order']
        
        # Convert MOPs
        mops = []
        for mop_data in data['mops']:
            if isinstance(mop_data['mop_type'], str):
                mop_data['mop_type'] = MOPType(mop_data['mop_type'])
            mops.append(MOPDefinition(**mop_data))
        data['mops'] = mops
        
        return ReleaseDefinition(**data)
    
    def render_release_documentation(self, release_version: str, variables_file: str) -> Dict[str, Any]:
        """Render all MOPs in a release to versioned documentation folders"""
        self.logger.log_system(f"Rendering documentation for release {release_version}", "render_release_docs")
        
        release = self.load_release_definition(release_version)
        
        # Create release documentation directory
        release_docs_path = self.base_docs_path / "releases" / release_version
        release_docs_path.mkdir(parents=True, exist_ok=True)
        
        # Create regional subdirectories
        for region in self.execution_order:
            (release_docs_path / region).mkdir(exist_ok=True)
        
        rendered_results = {}
        doc_renderer = DocumentationRenderer()
        
        # Load variables
        variables = doc_renderer.load_mop_variables(variables_file)
        
        for mop in release.mops:
            try:
                template_path = Path(mop.template_path)
                if not template_path.exists():
                    self.logger.log_system(f"Template not found: {template_path}", "template_missing", "error")
                    continue
                
                mop_results = {}
                
                # Render for each region
                for region in self.execution_order:
                    try:
                        rendered_content = doc_renderer.render_template_for_region(
                            template_path, region, variables
                        )
                        
                        # Save to regional folder
                        output_file = release_docs_path / region / f"{mop.id}.md"
                        with open(output_file, 'w') as f:
                            f.write(rendered_content)
                        
                        mop_results[region] = str(output_file)
                        
                    except Exception as e:
                        self.logger.log_system(f"Error rendering {mop.id} for {region}: {e}", "render_error", "error")
                        mop_results[region] = f"ERROR: {str(e)}"
                
                rendered_results[mop.id] = mop_results
                
            except Exception as e:
                self.logger.log_system(f"Error processing MOP {mop.id}: {e}", "mop_render_error", "error")
                rendered_results[mop.id] = {"error": str(e)}
        
        # Generate release index
        self.generate_release_index(release, release_docs_path, rendered_results)
        
        self.logger.log_system(f"Completed rendering for release {release_version}", "render_complete")
        return {
            "success": True,
            "release_version": release_version,
            "release_path": str(release_docs_path),
            "rendered_mops": rendered_results,
            "total_mops": len(release.mops),
            "regions": self.execution_order
        }
    
    def generate_release_index(self, release: ReleaseDefinition, release_path: Path, 
                             rendered_results: Dict[str, Any]):
        """Generate index page for the release"""
        index_content = [
            "---",
            f"title: Release {release.version} Documentation",
            f"description: {release.description}",
            f"version: {release.version}",
            f"created_at: {release.created_at}",
            f"created_by: {release.created_by}",
            f"total_mops: {len(release.mops)}",
            "layout: release_index",
            "---",
            "",
            f"# Release {release.version} Documentation",
            "",
            f"**Description**: {release.description}",
            f"**Created**: {release.created_at}",
            f"**Created By**: {release.created_by}",
            f"**Total MOPs**: {len(release.mops)}",
            "",
            "## Execution Order",
            "",
            "MOPs will be executed in the following regional order:",
        ]
        
        for i, region in enumerate(release.execution_order, 1):
            index_content.append(f"{i}. **{region.upper()}** - {self._get_region_description(region)}")
        
        index_content.extend([
            "",
            "## MOPs in this Release",
            ""
        ])
        
        # Group MOPs by type
        mops_by_type = {}
        for mop in release.mops:
            mop_type = mop.mop_type.value
            if mop_type not in mops_by_type:
                mops_by_type[mop_type] = []
            mops_by_type[mop_type].append(mop)
        
        for mop_type, mops in mops_by_type.items():
            index_content.extend([
                f"### {mop_type.title()} MOPs",
                ""
            ])
            
            for mop in mops:
                index_content.append(f"#### {mop.name} (`{mop.id}`)")
                index_content.append(f"- **Description**: {mop.description}")
                index_content.append(f"- **Risk Level**: {mop.risk_level}")
                index_content.append(f"- **Duration**: ~{mop.estimated_duration} minutes")
                index_content.append(f"- **Playbooks**: {', '.join(mop.playbooks)}")
                
                if mop.id in rendered_results:
                    index_content.append("- **Regional Documentation**:")
                    for region in release.execution_order:
                        if region in rendered_results[mop.id]:
                            doc_path = rendered_results[mop.id][region]
                            if not doc_path.startswith("ERROR:"):
                                rel_path = Path(doc_path).name
                                index_content.append(f"  - [{region.upper()}]({region}/{rel_path})")
                
                index_content.append("")
        
        # Save index
        index_path = release_path / "index.md"
        with open(index_path, 'w') as f:
            f.write('\n'.join(index_content))
    
    def _get_region_description(self, region: str) -> str:
        """Get description for a region"""
        descriptions = {
            "eus2": "East US 2 (Primary, Documentation Hub)",
            "wus2": "West US 2 (Primary West)",
            "wus3": "West US 3 (Modern Infrastructure)",
            "scus": "South Central US (Hub)",
            "eus2lea": "East US 2 LEA (Early Access)",
            "wus2lea": "West US 2 LEA (Early Access)"
        }
        return descriptions.get(region, f"{region.upper()} Region")
    
    def list_releases(self) -> List[Dict[str, Any]]:
        """List all available releases"""
        releases = []
        config_dir = self.releases_path / "configs"
        
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                try:
                    release = self.load_release_definition(config_file.stem)
                    releases.append({
                        "version": release.version,
                        "description": release.description,
                        "created_at": release.created_at,
                        "created_by": release.created_by,
                        "status": release.status.value,
                        "total_mops": len(release.mops),
                        "current_region": release.current_region,
                        "current_mop": release.current_mop
                    })
                except Exception as e:
                    self.logger.log_system(f"Error loading release {config_file.stem}: {e}", "load_release_error", "error")
        
        # Sort by version (newest first)
        releases.sort(key=lambda x: x['created_at'], reverse=True)
        return releases

def create_release_from_vendor_mops(vendor_dir: str, release_version: str, 
                                   variables_file: str, description: str = "", 
                                   created_by: str = "system") -> Dict[str, Any]:
    """Main function to create and render a complete MOP release"""
    manager = MOPReleaseManager()
    
    try:
        # Process vendor MOPs
        release = manager.process_vendor_mops(vendor_dir, release_version, description, created_by)
        
        # Render documentation
        render_result = manager.render_release_documentation(release_version, variables_file)
        
        return {
            "success": True,
            "release": {
                "version": release.version,
                "description": release.description,
                "total_mops": len(release.mops),
                "mop_types": list(set(mop.mop_type.value for mop in release.mops))
            },
            "documentation": render_result,
            "message": f"Successfully created release {release_version} with {len(release.mops)} MOPs"
        }
    
    except Exception as e:
        manager.logger.log_system(str(e), "create_release_error", "error")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    result = create_release_from_vendor_mops(
        "templates/vendor", 
        "R11.5.3.3", 
        "example-agent-upgrade.yml",
        "Example release with vendor MOPs"
    )
    print(json.dumps(result, indent=2))