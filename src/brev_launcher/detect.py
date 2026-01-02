"""Detection logic for project type and entry files."""

import re
import subprocess
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


def detect_current_gpu() -> str:
    """Detect GPU type from nvidia-smi on current machine.
    
    Returns:
        Brev GPU type string (e.g., 'gpu_1x_a10') or 'any' if not detected.
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode != 0:
            return "any"
        
        gpu_name = result.stdout.strip().lower()
        
        # Map GPU names to Brev GPU types
        if "a10" in gpu_name:
            return "gpu_1x_a10"
        elif "a100" in gpu_name:
            if "80gb" in gpu_name:
                return "gpu_1x_a100_80gb"
            return "gpu_1x_a100"
        elif "t4" in gpu_name:
            return "gpu_1x_t4"
        elif "v100" in gpu_name:
            return "gpu_1x_v100"
        elif "h100" in gpu_name:
            return "gpu_1x_h100"
        else:
            return "any"
            
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return "any"


def get_gpu_memory_gb() -> Optional[float]:
    """Get GPU memory in GB from nvidia-smi.
    
    Returns:
        GPU memory in GB, or None if not available.
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode != 0:
            return None
        
        # Memory is returned in MiB, convert to GB
        memory_mib = float(result.stdout.strip())
        return round(memory_mib / 1024, 1)
        
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ValueError):
        return None


def estimate_vram_usage(path: Path = Path.cwd()) -> Optional[float]:
    """Estimate VRAM usage by scanning code and dependencies.
    
    Looks for common ML models and frameworks to estimate memory requirements.
    
    Args:
        path: Project directory path.
        
    Returns:
        Estimated VRAM in GB, or None if cannot estimate.
    """
    result = estimate_vram_usage_detailed(path)
    return result["estimated_vram"] if result else None


def estimate_vram_usage_detailed(path: Path = Path.cwd()) -> Optional[dict]:
    """Estimate VRAM usage with detailed detection information.
    
    Args:
        path: Project directory path.
        
    Returns:
        Dictionary with:
        - estimated_vram: float (final estimate with buffer)
        - base_vram: float (base model requirement)
        - detected_models: list of {model, vram, file}
        - frameworks: list of detected frameworks
        Or None if cannot estimate.
    """
    # Model size patterns (model name -> estimated VRAM in GB)
    model_patterns = {
        # LLM models
        r'gpt-?2|gpt2': ("GPT-2", 2.0),
        r'gpt-?3\.5|gpt3': ("GPT-3.5", 4.0),
        r'llama.*7b|7b.*model|7b.*llm': ("LLaMA 7B", 14.0),
        r'llama.*13b|13b.*model': ("LLaMA 13B", 26.0),
        r'llama.*70b|70b.*model': ("LLaMA 70B", 140.0),
        r'mistral.*7b': ("Mistral 7B", 14.0),
        r'mixtral.*8x7b': ("Mixtral 8x7B", 90.0),
        
        # Stable Diffusion
        r'stable.*diffusion.*1\.5|sd.*1\.5|runwayml': ("Stable Diffusion 1.5", 6.0),
        r'stable.*diffusion.*xl|sdxl': ("Stable Diffusion XL", 12.0),
        r'stable.*diffusion.*2|sd.*2\.': ("Stable Diffusion 2", 8.0),
        
        # Whisper models
        r'whisper.*large': ("Whisper Large", 10.0),
        r'whisper.*medium': ("Whisper Medium", 5.0),
        r'whisper.*small': ("Whisper Small", 2.0),
        r'whisper.*base': ("Whisper Base", 1.0),
        
        # Other common models
        r'bert.*large': ("BERT Large", 3.0),
        r'bert.*base': ("BERT Base", 1.5),
        r't5.*large': ("T5 Large", 3.0),
        r't5.*xl': ("T5 XL", 11.0),
        r'yolo.*v8': ("YOLOv8", 2.0),
        r'sam|segment.*anything': ("Segment Anything (SAM)", 6.0),
    }
    
    detected_models = []
    max_vram = 0.0
    frameworks = set()
    
    # Scan Python files
    for py_file in path.rglob("*.py"):
        if py_file.name.startswith("."):
            continue
        try:
            content = py_file.read_text(errors='ignore').lower()
            for pattern, (model_name, vram) in model_patterns.items():
                if re.search(pattern, content):
                    detected_models.append({
                        "model": model_name,
                        "vram": vram,
                        "file": str(py_file.relative_to(path)),
                    })
                    max_vram = max(max_vram, vram)
            
            # Detect frameworks
            if 'import torch' in content or 'from torch' in content:
                frameworks.add('PyTorch')
            if 'import tensorflow' in content or 'from tensorflow' in content:
                frameworks.add('TensorFlow')
            if 'import jax' in content or 'from jax' in content:
                frameworks.add('JAX')
            if 'from diffusers' in content or 'import diffusers' in content:
                frameworks.add('Diffusers')
            if 'import transformers' in content or 'from transformers' in content:
                frameworks.add('Transformers')
        except Exception:
            continue
    
    # Scan requirements.txt
    req_file = path / "requirements.txt"
    if req_file.exists():
        try:
            content = req_file.read_text(errors='ignore').lower()
            for pattern, (model_name, vram) in model_patterns.items():
                if re.search(pattern, content):
                    detected_models.append({
                        "model": model_name,
                        "vram": vram,
                        "file": "requirements.txt",
                    })
                    max_vram = max(max_vram, vram)
            
            # Detect frameworks in requirements
            if 'torch' in content:
                frameworks.add('PyTorch')
            if 'tensorflow' in content:
                frameworks.add('TensorFlow')
            if 'diffusers' in content:
                frameworks.add('Diffusers')
            if 'transformers' in content:
                frameworks.add('Transformers')
        except Exception:
            pass
    
    # Scan pyproject.toml
    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(errors='ignore').lower()
            for pattern, (model_name, vram) in model_patterns.items():
                if re.search(pattern, content):
                    detected_models.append({
                        "model": model_name,
                        "vram": vram,
                        "file": "pyproject.toml",
                    })
                    max_vram = max(max_vram, vram)
        except Exception:
            pass
    
    # Check for common frameworks (gives us a baseline)
    if max_vram == 0:
        try:
            all_content = ""
            if req_file.exists():
                all_content += req_file.read_text(errors='ignore').lower()
            if pyproject.exists():
                all_content += pyproject.read_text(errors='ignore').lower()
            
            # If has torch/tensorflow but no specific model, estimate 4GB baseline
            if any(fw in all_content for fw in ['torch', 'tensorflow', 'jax']):
                max_vram = 4.0
                detected_models.append({
                    "model": "Generic ML Framework",
                    "vram": 4.0,
                    "file": "requirements.txt (baseline)",
                })
        except Exception:
            pass
    
    # Return None if no models detected
    if max_vram == 0:
        return None
    
    # Add 50% buffer for safety (gradients, activations, etc.)
    estimated_vram = round(max_vram * 1.5, 1)
    
    # Deduplicate detected models (keep unique by model name)
    unique_models = {}
    for detection in detected_models:
        model_name = detection["model"]
        if model_name not in unique_models or detection["vram"] > unique_models[model_name]["vram"]:
            unique_models[model_name] = detection
    
    return {
        "estimated_vram": estimated_vram,
        "base_vram": max_vram,
        "detected_models": list(unique_models.values()),
        "frameworks": sorted(list(frameworks)),
    }

