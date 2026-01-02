"""Project scanning and metadata collection."""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .detect import (
    detect_current_gpu,
    detect_dependency_file,
    detect_entry_file,
    detect_env_example,
    detect_notebooks_folder,
    detect_ports_in_code,
    get_gpu_memory_gb,
    get_install_command,
    infer_project_type,
)
from .gitinfo import GitInfo, get_git_info


@dataclass
class BrevInfo:
    """Information from Brev CLI and environment."""

    available: bool = False
    instance_name: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_memory_gb: Optional[float] = None
    status: Optional[str] = None


@dataclass
class ProjectScan:
    """Complete project scan results."""

    path: Path
    git: GitInfo
    dependency_file: Optional[str] = None
    entry_file: Optional[str] = None
    has_env_example: bool = False
    has_notebooks_folder: bool = False
    detected_ports: list[int] = field(default_factory=list)
    inferred_type: str = "notebook"
    install_command: str = ""
    brev: BrevInfo = field(default_factory=BrevInfo)


def check_brev_cli() -> BrevInfo:
    """Check if Brev CLI is available and get instance info.
    
    Also detects GPU from nvidia-smi even if Brev CLI is not available.
    """
    info = BrevInfo()
    
    # Always try to detect GPU from nvidia-smi
    info.gpu_type = detect_current_gpu()
    info.gpu_memory_gb = get_gpu_memory_gb()

    try:
        # Check if brev command exists
        result = subprocess.run(
            ["which", "brev"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return info

        info.available = True

        # Try to get instance name from brev ls
        result = subprocess.run(
            ["brev", "ls"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            # Parse output to find current instance
            # This is best-effort; format may vary
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if "*" in line or "RUNNING" in line.upper():
                    # Try to extract instance name
                    parts = line.split()
                    if len(parts) >= 2:
                        # Skip markers like * and status indicators
                        for part in parts:
                            if part not in ("*", "RUNNING", "STOPPED", "CREATING"):
                                info.instance_name = part
                                break
                        # Try to extract status
                        if "RUNNING" in line.upper():
                            info.status = "RUNNING"
                        break

    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return info


def scan_project(path: Path = Path.cwd()) -> ProjectScan:
    """Scan the project directory and collect all metadata.

    Args:
        path: Project directory path.

    Returns:
        ProjectScan with all collected information.

    Raises:
        GitError: If not a git repo or origin is missing.
    """
    git_info = get_git_info(path)

    dependency_file = detect_dependency_file(path)
    inferred_type = infer_project_type(path)
    entry_file = detect_entry_file(path, inferred_type)

    return ProjectScan(
        path=path,
        git=git_info,
        dependency_file=dependency_file,
        entry_file=entry_file,
        has_env_example=detect_env_example(path),
        has_notebooks_folder=detect_notebooks_folder(path),
        detected_ports=detect_ports_in_code(path),
        inferred_type=inferred_type,
        install_command=get_install_command(dependency_file),
        brev=check_brev_cli(),
    )

