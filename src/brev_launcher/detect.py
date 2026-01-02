"""Detection logic for project type and entry files."""

import re
from pathlib import Path
from typing import Optional

from .constants import (
    COMMON_APP_PORTS,
    NOTEBOOK_ENTRY_FILES,
    WEBAPP_ENTRY_FILES,
)


def detect_dependency_file(path: Path = Path.cwd()) -> Optional[str]:
    """Detect the dependency file in the project.

    Returns:
        Path to requirements.txt or pyproject.toml if found, None otherwise.
    """
    requirements = path / "requirements.txt"
    if requirements.exists():
        return "requirements.txt"

    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        return "pyproject.toml"

    return None


def detect_entry_file(path: Path = Path.cwd(), project_type: str = "notebook") -> Optional[str]:
    """Detect the entry file based on project type.

    Args:
        path: Project directory path.
        project_type: Either 'notebook' or 'webapp'.

    Returns:
        Entry file name if found, None otherwise.
    """
    if project_type == "notebook":
        # Check prioritized notebook files
        for notebook in NOTEBOOK_ENTRY_FILES:
            if (path / notebook).exists():
                return notebook

        # Look for any .ipynb file
        notebooks = list(path.glob("*.ipynb"))
        if notebooks:
            return notebooks[0].name

    else:  # webapp
        # Check prioritized webapp files
        for entry in WEBAPP_ENTRY_FILES:
            if (path / entry).exists():
                return entry

        # Look for any .py file as fallback
        py_files = list(path.glob("*.py"))
        if py_files:
            return py_files[0].name

    return None


def find_candidate_entry_files(path: Path = Path.cwd()) -> list[str]:
    """Find all candidate entry files in the project.

    Returns:
        List of potential entry file names.
    """
    candidates = []

    # Add notebooks
    for notebook in path.glob("*.ipynb"):
        candidates.append(notebook.name)

    # Add Python files
    for py_file in path.glob("*.py"):
        # Skip test files and __init__.py
        if not py_file.name.startswith("test_") and py_file.name != "__init__.py":
            candidates.append(py_file.name)

    return sorted(candidates)


def detect_env_example(path: Path = Path.cwd()) -> bool:
    """Check if .env.example exists."""
    return (path / ".env.example").exists()


def detect_notebooks_folder(path: Path = Path.cwd()) -> bool:
    """Check if a notebooks folder exists."""
    notebooks_dir = path / "notebooks"
    return notebooks_dir.exists() and notebooks_dir.is_dir()


def detect_ports_in_code(path: Path = Path.cwd()) -> list[int]:
    """Detect common ports mentioned in Python files.

    This is a heuristic that looks for port patterns in code.
    """
    detected_ports = set()

    # Pattern to match port assignments or arguments
    port_patterns = [
        r"port\s*=\s*(\d+)",
        r"PORT\s*=\s*(\d+)",
        r"--port[=\s]+(\d+)",
        r":(\d+)",
    ]

    for py_file in path.glob("*.py"):
        try:
            content = py_file.read_text()
            for pattern in port_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    port = int(match)
                    if port in COMMON_APP_PORTS:
                        detected_ports.add(port)
        except (OSError, ValueError):
            continue

    return sorted(detected_ports)


def get_install_command(dependency_file: Optional[str]) -> str:
    """Get the appropriate install command based on dependency file.

    Args:
        dependency_file: Name of the dependency file.

    Returns:
        Install command string.
    """
    if dependency_file == "requirements.txt":
        return "pip install -r requirements.txt"
    elif dependency_file == "pyproject.toml":
        return "pip install ."
    else:
        return "# No dependency file found - add install commands here"


def infer_project_type(path: Path = Path.cwd()) -> str:
    """Infer project type based on files present.

    Returns:
        'notebook' if notebooks are present, 'webapp' otherwise.
    """
    # Check for notebooks
    notebooks = list(path.glob("*.ipynb"))
    if notebooks:
        return "notebook"

    # Check for webapp entry files
    for entry in WEBAPP_ENTRY_FILES:
        if (path / entry).exists():
            return "webapp"

    # Default to notebook
    return "notebook"

