"""Pydantic schemas for Brev Launchable configuration."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    """Git source configuration."""

    type: str = "git"
    url: str
    ref: str = "main"
    path: str = "/"


class SetupConfig(BaseModel):
    """Setup/installation configuration."""

    python_version: str = "3.10"
    install: str = "pip install -r requirements.txt"


class NotebookConfig(BaseModel):
    """Notebook runtime configuration."""

    enable_jupyter: bool = True
    command: str = "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
    port: int = 8888


class WebappConfig(BaseModel):
    """Webapp runtime configuration."""

    expose_port: int = 7860
    command: str = "python app.py"


class StartConfig(BaseModel):
    """Start configuration - either notebook or webapp."""

    notebook: Optional[NotebookConfig] = None
    webapp: Optional[WebappConfig] = None


class RuntimeConfig(BaseModel):
    """Runtime configuration."""

    mode: str = "vm"
    setup: SetupConfig = Field(default_factory=SetupConfig)
    start: StartConfig = Field(default_factory=StartConfig)


class ComputeConfig(BaseModel):
    """Compute/GPU configuration."""

    gpu: str = "any"
    note: str = "Select lowest-cost GPU in Brev UI"


class NetworkingConfig(BaseModel):
    """Networking/port configuration."""

    ports: list[int] = Field(default_factory=list)


class FilesConfig(BaseModel):
    """Files configuration."""

    include: list[str] = Field(default_factory=lambda: ["."])


class MetadataConfig(BaseModel):
    """Metadata about generation."""

    generated_by: str = "brev-launcher"
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )


class LaunchableConfig(BaseModel):
    """Complete Brev Launchable configuration."""

    name: str
    description: str
    source: SourceConfig
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    compute: ComputeConfig = Field(default_factory=ComputeConfig)
    networking: NetworkingConfig = Field(default_factory=NetworkingConfig)
    files: FilesConfig = Field(default_factory=FilesConfig)
    metadata: MetadataConfig = Field(default_factory=MetadataConfig)

    def with_notebook(
        self,
        command: str = "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser",
        port: int = 8888,
    ) -> "LaunchableConfig":
        """Configure for notebook mode."""
        self.runtime.start.notebook = NotebookConfig(
            enable_jupyter=True,
            command=command,
            port=port,
        )
        self.runtime.start.webapp = None
        if port not in self.networking.ports:
            self.networking.ports.append(port)
        return self

    def with_webapp(
        self,
        command: str = "python app.py",
        port: int = 7860,
    ) -> "LaunchableConfig":
        """Configure for webapp mode."""
        self.runtime.start.webapp = WebappConfig(
            expose_port=port,
            command=command,
        )
        self.runtime.start.notebook = None
        if port not in self.networking.ports:
            self.networking.ports.append(port)
        return self

    def with_install_command(self, command: str) -> "LaunchableConfig":
        """Set the install command."""
        self.runtime.setup.install = command
        return self

