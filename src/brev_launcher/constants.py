"""Constants used throughout brev-launcher."""

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILURE = 2
EXIT_GENERATION_FAILURE = 3

# Default ports
DEFAULT_JUPYTER_PORT = 8888
DEFAULT_WEBAPP_PORT = 7860

# Default commands
DEFAULT_NOTEBOOK_COMMAND = "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
DEFAULT_WEBAPP_COMMAND = "python app.py"

# Project types
PROJECT_TYPE_NOTEBOOK = "notebook"
PROJECT_TYPE_WEBAPP = "webapp"

# File names
LAUNCHABLE_YAML = "launchable.yaml"
REQUIREMENTS_TXT = "requirements.txt"
PYPROJECT_TOML = "pyproject.toml"
ENV_EXAMPLE = ".env.example"

# Entry file priorities
NOTEBOOK_ENTRY_FILES = ["main.ipynb", "notebook.ipynb", "demo.ipynb"]
WEBAPP_ENTRY_FILES = ["app.py", "main.py", "server.py", "api.py"]

# Common ports to detect in code
COMMON_APP_PORTS = [7860, 8000, 8080, 5000, 3000, 8501, 8502]

# Brev URLs
BREV_DEPLOY_BADGE_URL = "https://brev.nvidia.com/assets/deploy-badge.svg"
BREV_DEPLOY_URL_TEMPLATE = "https://brev.nvidia.com/launchables/{launchable_id}/deploy"

# Default Python version
DEFAULT_PYTHON_VERSION = "3.10"

# Default GPU placeholder
DEFAULT_GPU_PLACEHOLDER = "any"
DEFAULT_GPU_NOTE = "Select lowest-cost GPU in Brev UI"

