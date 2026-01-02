# brev-launcher

Generate Brev Launchable config files from your project with a single command.

[![Deploy on Brev](https://brev.nvidia.com/assets/deploy-badge.svg)](https://brev.nvidia.com/launchables/env-REPLACE_ME/deploy)

## Overview

`brev-launcher` scans your project, detects its configuration, and generates a `launchable.yaml` file that you can use to deploy on [Brev](https://brev.nvidia.com) with one click.

### Features

- **Auto-detection**: Detects project type (notebook/webapp), dependencies, and entry files
- **Git-aware**: Extracts repository URL and normalizes it for Brev
- **Minimal prompts**: Only asks essential questions with smart defaults
- **Stable output**: Generates reproducible YAML with consistent ordering
- **Badge generation**: Creates ready-to-use deploy badges for your README

## Installation

```bash
pip install brev-launcher
```

Or install from source:

```bash
git clone https://github.com/brevdev/brev-launcher.git
cd brev-launcher
pip install -e .
```

## Quick Start

```bash
# Navigate to your project
cd my-gpu-project

# Generate launchable.yaml
brev-launcher init

# Follow the printed instructions to deploy on Brev
```

## Commands

### `brev-launcher init`

Initialize a Brev Launchable config for your project.

```bash
# Interactive mode (default)
brev-launcher init

# Non-interactive mode with defaults
brev-launcher init --non-interactive

# Specify project type
brev-launcher init --type notebook
brev-launcher init --type webapp --port 8080

# Different directory
brev-launcher init /path/to/project
```

**What it does:**

1. **Validates** your git repository setup
2. **Detects** project type, dependencies, and entry files
3. **Asks** minimal questions (project type, port, start command)
4. **Generates** `launchable.yaml`
5. **Prints** next steps and badge snippet

### `brev-launcher doctor`

Check your project's health and Brev compatibility.

```bash
brev-launcher doctor
```

Runs checks for:
- Git repository setup
- Origin remote configuration
- Dependency files (requirements.txt / pyproject.toml)
- Entry files detection
- Existing launchable.yaml

### `brev-launcher print-badge`

Generate a deploy badge snippet for your README.

```bash
# With placeholder ID
brev-launcher print-badge

# With your actual Launchable ID
brev-launcher print-badge abc123-your-launchable-id
```

## Generated `launchable.yaml`

The generated config includes:

```yaml
name: my-project
description: my-project - deployed via Brev Launchables

source:
  type: git
  url: https://github.com/user/my-project
  ref: main
  path: /

runtime:
  mode: vm
  setup:
    python_version: "3.10"
    install: pip install -r requirements.txt
  start:
    notebook:
      enable_jupyter: true
      command: jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
      port: 8888

compute:
  gpu: any
  note: Select lowest-cost GPU in Brev UI

networking:
  ports:
    - 8888

files:
  include:
    - "."

metadata:
  generated_by: brev-launcher
  generated_at: 2024-01-15T10:30:00+00:00
```

## Requirements

- **Python 3.10+**
- **Git repository** with a public origin remote
- Either `requirements.txt` or `pyproject.toml` (recommended)

## Project Types

### Notebook Projects

Default for projects containing `.ipynb` files.

- Enables JupyterLab
- Default port: 8888
- Default command: `jupyter lab --ip=0.0.0.0 --port=8888 --no-browser`

### Webapp Projects

For Flask, FastAPI, Gradio, Streamlit, etc.

- Exposes specified port
- Default port: 7860 (Gradio default)
- Default command: `python app.py`

## Example Project

See the [`example-project/`](./example-project/) directory for a complete example:

```bash
cd example-project
brev-launcher init --non-interactive
```

## Workflow

1. **Develop** your project locally
2. **Push** to a public GitHub repository
3. **Run** `brev-launcher init` to generate config
4. **Commit** `launchable.yaml` to your repo
5. **Create** a Launchable in the Brev console:
   - Go to **Launchables** → **Create Launchable**
   - Select **Git Repository**
   - Click **Show configuration**
   - Paste your `launchable.yaml` contents
6. **Deploy** and enjoy GPU-powered development!

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Validation failure (e.g., not a git repo) |
| 3 | Generation failure |

## Development

### Setup

```bash
# Clone the repo
git clone https://github.com/brevdev/brev-launcher.git
cd brev-launcher

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Style

```bash
# Format code
ruff format src tests

# Lint
ruff check src tests
```

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

Built with ❤️ for the GPU development community.
