# mop_ansible_renderer/README.md

# MOP-Driven Ansible Automation Platform

This application automates the rendering, classification, and execution of Markdown-based operational procedures ("MOPs") using a **Flask backend**, a **Next.js frontend**, and **Ansible orchestration**. It is designed for Azure infrastructure environments, especially where operations are managed via Infrastructure-as-Code (IaC), GitOps, and Azure DevOps pipelines.

---

## 🎯 Purpose

This system replaces manual MOP execution with:
- Jinja2-rendered markdown files with YAML frontmatter
- Frontmatter-linked Ansible playbooks
- Optional GitOps workflows (edit/commit/push vars to repo)
- Azure DevOps pipeline triggers
- Flask API and Next.js UI for management and transparency

---

## 📐 Architecture

### Components:

- **Flask Backend**
  - Serves MOPs via REST API
  - Renders Jinja2 templates using region-scoped vars
  - Handles MOP execution (via Ansible subprocess)
  - Logs output and retry metadata

- **Next.js Frontend**
  - Fetches MOPs from Flask API
  - Displays Markdown with frontmatter and playbooks
  - Allows execution of MOPs via UI (button or form)
  - Shows logs and run history for each MOP

- **Jinja2 MOP Templates**
  - Markdown files with `{{ variable }}` syntax
  - Rendered with per-MOP YAML files

- **YAML Variable Files** (`/vars/*.yml`)
  - Define MOP metadata (id, title, category, parameters)
  - Drive what template and playbooks to use

- **Category-to-Playbook Map** (`category_map.py`)
  - Associates each category with 1–N playbooks

- **Ansible Playbooks** (`/playbooks/*.yml`)
  - Reusable modular playbooks like:
    - `patch_linux.yml`
    - `edit_yaml.yml`
    - `run_manual_pipeline.yml`
    - `commit_to_git.yml`

- **Execution Logging** (`/logs/*.json`)
  - Stores status, return code, timestamp per MOP execution

---

## ⚙️ Example Workflow

### 1. Define MOP Variable File
```yaml
# vars/mop-eus2-linux-patch-001.yml
id: mop-eus2-linux-patch-001
title: "Patch Critical Linux VMs"
category: patch-linux
region: eastus2
patch_group: critical
```

### 2. Category Map
```python
# category_map.py
CATEGORY_TO_PLAYBOOK = {
  "patch-linux": ["patch_linux.yml"],
  "agent-upgrade": ["edit_yaml.yml", "commit_to_git.yml", "run_manual_pipeline.yml"],
  "pipeline-only": ["run_manual_pipeline.yml"]
}
```

### 3. Render Frontmatter + Markdown (via Jinja2)
```markdown
---
title: {{ title }}
id: {{ id }}
category: {{ category }}
region: {{ region }}
playbooks:
{% for pb in playbooks %}  - {{ pb }}
{% endfor %}
parameters:
  patch_group: {{ patch_group }}
---

# {{ title }}

This MOP executes automated patching...
```

### 4. Flask API Endpoint
```http
POST /api/mops/mop-eus2-linux-patch-001/execute
```

### 5. Execution Output
Stored in `/logs/mop-eus2-linux-patch-001_<timestamp>.json`

### 6. UI via Next.js
- Operator selects MOP, previews it, and clicks Run
- See live status and log updates on screen

---

## 🧠 Design Decisions

- MOPs are categorized, and categories drive Ansible playbook routing
- Jinja render process injects YAML frontmatter
- Execution handled via `subprocess.run(["ansible-playbook", ...])`
- Errors are logged; retries allowed
- Next.js UI improves observability and ease-of-use

---

## 📁 File Tree Structure
```
mop_ansible_renderer/
├── app.py              # Flask app
├── templates/
│   ├── patch_linux.md.j2
│   └── agent_upgrade.md.j2
├── vars/
│   └── mop-eus2-linux-patch-001.yml
├── playbooks/
│   ├── patch_linux.yml
│   ├── edit_yaml.yml
│   ├── commit_to_git.yml
│   └── run_manual_pipeline.yml
├── logs/
├── category_map.py
├── renderer.py         # Jinja render logic
├── executor.py         # Ansible execution logic
├── frontend/           # Next.js frontend directory
│   ├── pages/
│   │   ├── index.tsx           # Homepage with MOP list
│   │   └── [mopId].tsx         # Dynamic MOP execution page
│   ├── components/
│   │   ├── MopCard.tsx         # Preview MOP info
│   │   ├── ExecutionLog.tsx    # Show logs
│   │   └── Header.tsx          # Common layout/header
│   └── public/
│       └── styles.css
└── README.md
```

---

## 🚀 Replit Instructions

1. Clone or create a Replit project with this structure
2. Set up the Python environment and install Flask, Jinja2, etc.
3. Add your MOP `.yml` files under `/vars`
4. Run Flask backend with `app.py`
5. Deploy the Next.js frontend from `/frontend`
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
6. Access the frontend UI at `http://localhost:3000`

---

## ✅ Outcome

By moving to this platform, your team can:
- Replace 25 manual MOPs per region with ~12 core playbooks
- Dynamically render MOPs based on region and metadata
- Integrate IaC, Git, DevOps, and documentation into a single automation stream
- Provide a self-service web UI for operations
- Ensure repeatability, auditability, and faster change control cycles
