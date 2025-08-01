# Overview

This is a MOP (Method of Procedure) Automation Platform that automates the rendering, classification, and execution of Markdown-based operational procedures using a Flask backend, Next.js frontend, and Ansible orchestration. The system replaces manual MOP execution with an automated workflow that renders Jinja2 templates, executes Ansible playbooks based on categories, and provides both web interfaces for management and monitoring.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes

## MOP Release Management System (August 2025)
- **Status**: Completed - Full release management platform for vendor MOPs
- **Capabilities**: Type detection, automated playbook assignment, regional rendering
- **Version Control**: Releases with version folders (e.g., R11.5.3.3) and regional subfolders
- **Execution Management**: Sequential execution framework with observability controls
- **Documentation**: Automated generation of regional MOP documentation with frontmatter metadata
- **Safety Controls**: Careful execution management to prevent unexpected automation runs
- **MOP Types**: Agent upgrade, infrastructure, patch-linux, network security, database maintenance
- **Integration**: Complete web interface for release creation and management

## Azure Multi-Region Ansible Configuration (August 2025)
- **Status**: Completed - Full six-region Azure configuration with Ansible inventory
- **Regions**: eus2, wus2, wus3, scus, eus2lea, wus2lea with separate ADO organizations
- **Infrastructure**: Regional inventory, host groups, network configuration per region
- **Azure DevOps**: Each region has its own ADO organization, project, pipelines, and environments
- **LEA Support**: Special handling for Early Access regions (eus2lea, wus2lea)
- **Security**: Complete organizational isolation, separate PAT tokens, dedicated subscriptions

## Comprehensive Logging System with Ansible Integration (August 2025)
- **Status**: Completed - Full logging infrastructure with comprehensive Ansible integration
- **Components**: MOPLogger class with process, execution, system, and Ansible logging
- **Ansible Integration**: Captures STDOUT, STDERR, log files, JSON callbacks, and performance data
- **API Integration**: Complete RESTful logging API with specialized Ansible endpoints
- **Dashboard**: Web-based logs dashboard with dedicated Ansible log viewer and analysis
- **Features**: Process tracking, execution monitoring, error logging, log search, and Ansible performance analysis
- **Log Types**: System logs, execution logs, process logs, and comprehensive Ansible logs with timing data

## Next.js Frontend Integration (January 2025)
- **Status**: Completed - Full Next.js frontend with TypeScript configuration
- **Architecture**: Dual interface system with Flask backend API and Next.js frontend
- **API Integration**: RESTful endpoints with proper proxy configuration
- **Error Handling**: Improved execution error reporting with development environment considerations
- **Demo Interface**: Created integration demo page showing system readiness

# System Architecture

## Frontend Architecture
- **Next.js Frontend**: Modern React-based interface for MOP management and execution
- **Flask Web Application**: Serves as admin interface with Bootstrap-based responsive UI for configuration
- **Template Engine**: Jinja2 for rendering both web templates and MOP content
- **Static Assets**: CSS/JS for enhanced user experience with CodeMirror integration for code editing
- **Navigation Structure**: Dual interface - Next.js for operations, Flask for administration

## Backend Architecture
- **Flask Application**: Core web server handling routing, templating, and API endpoints
- **MOP Renderer**: Handles Jinja2 template rendering using YAML variable files
- **MOP Executor**: Manages Ansible playbook execution with logging and status tracking
- **Category Mapping**: Configuration system that maps MOP categories to specific Ansible playbooks

## Data Storage Solutions
- **File-based Storage**: 
  - YAML variable files in `/vars/` directory for MOP configuration
  - Jinja2 templates for MOP content rendering
  - JSON execution logs in `/logs/` directory
  - Ansible playbooks in `/playbooks/` directory

## Authentication and Authorization
- **Session Management**: Flask session handling with configurable secret key
- **Basic Security**: Environment-based configuration for production deployment

## Execution Workflow
- **Category-based Execution**: MOPs are categorized (patch-linux, agent-upgrade, pipeline-only, git-ops, infrastructure)
- **Multi-playbook Support**: Each category can trigger multiple Ansible playbooks in sequence
- **Logging and Monitoring**: Comprehensive execution tracking with timestamps and status codes
- **Error Handling**: Graceful degradation with continued execution of remaining playbooks on failure

## Design Patterns
- **Component Separation**: Clear separation between rendering, execution, and web interface concerns
- **Configuration-driven**: Category-to-playbook mapping allows easy extension without code changes
- **Template-based**: Jinja2 templates provide flexible content generation with variable substitution

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web framework for the application server
- **Jinja2**: Template engine for both web UI and MOP content rendering
- **PyYAML**: YAML parsing for configuration and variable files

## Frontend Dependencies
- **Bootstrap**: CSS framework for responsive UI design
- **Font Awesome**: Icon library for enhanced visual interface
- **CodeMirror**: Code editor for YAML and template editing with syntax highlighting

## Infrastructure Dependencies
- **Ansible**: Automation engine for executing operational procedures
- **Git**: Version control system for GitOps workflows (referenced in playbooks)
- **Azure DevOps**: Pipeline execution system for infrastructure automation

## File System Requirements
- **Directory Structure**: Requires specific directories for logs, vars, playbooks, and templates
- **YAML Configuration**: Variable files drive MOP behavior and playbook selection
- **Template Storage**: Jinja2 templates stored in file system for rendering

## Optional Integrations
- **GitOps Workflow**: Automated git operations for infrastructure-as-code workflows
- **Pipeline Triggers**: Integration with Azure DevOps for automated deployments
- **Linux Patching**: System-level operations for server maintenance