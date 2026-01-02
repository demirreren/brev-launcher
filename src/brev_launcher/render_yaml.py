"""YAML rendering with stable ordering."""

from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .constants import LAUNCHABLE_YAML
from .launchable_schema import LaunchableConfig


def _ordered_dict_from_config(config: LaunchableConfig) -> dict[str, Any]:
    """Convert LaunchableConfig to an ordered dict for YAML output.

    Ensures stable key ordering for reproducible output.
    """
    result: dict[str, Any] = {}

    # Top-level fields in desired order
    result["name"] = config.name
    result["description"] = config.description

    # Source section
    result["source"] = {
        "type": config.source.type,
        "url": config.source.url,
        "ref": config.source.ref,
        "path": config.source.path,
    }

    # Runtime section
    runtime: dict[str, Any] = {
        "mode": config.runtime.mode,
        "setup": {
            "python_version": config.runtime.setup.python_version,
            "install": config.runtime.setup.install,
        },
    }

    # Start config - only include the active mode
    start: dict[str, Any] = {}
    if config.runtime.start.notebook:
        nb = config.runtime.start.notebook
        start["notebook"] = {
            "enable_jupyter": nb.enable_jupyter,
            "command": nb.command,
            "port": nb.port,
        }
    if config.runtime.start.webapp:
        wa = config.runtime.start.webapp
        start["webapp"] = {
            "expose_port": wa.expose_port,
            "command": wa.command,
        }
    runtime["start"] = start
    result["runtime"] = runtime

    # Compute section
    result["compute"] = {
        "gpu": config.compute.gpu,
        "note": config.compute.note,
    }

    # Networking section
    result["networking"] = {
        "ports": config.networking.ports,
    }

    # Files section
    result["files"] = {
        "include": config.files.include,
    }

    # Metadata section
    result["metadata"] = {
        "generated_by": config.metadata.generated_by,
        "generated_at": config.metadata.generated_at,
    }

    return result


def render_yaml(config: LaunchableConfig) -> str:
    """Render LaunchableConfig to YAML string.

    Uses ruamel.yaml for stable output with:
    - 2-space indentation
    - Preserved key ordering
    - Human-readable format
    """
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    ordered_data = _ordered_dict_from_config(config)

    stream = StringIO()
    yaml.dump(ordered_data, stream)
    return stream.getvalue()


def write_launchable_yaml(config: LaunchableConfig, path: Path = Path.cwd()) -> Path:
    """Write LaunchableConfig to launchable.yaml file.

    Args:
        config: The configuration to write.
        path: Directory to write the file in.

    Returns:
        Path to the written file.
    """
    yaml_content = render_yaml(config)
    output_path = path / LAUNCHABLE_YAML
    output_path.write_text(yaml_content)
    return output_path

