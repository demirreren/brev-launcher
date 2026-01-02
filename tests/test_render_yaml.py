"""Tests for render_yaml module."""

from pathlib import Path

import pytest

from brev_launcher.launchable_schema import LaunchableConfig, SourceConfig
from brev_launcher.render_yaml import render_yaml, write_launchable_yaml


class TestRenderYaml:
    """Tests for render_yaml function."""

    def test_basic_render(self) -> None:
        """Should render basic config to YAML."""
        config = LaunchableConfig(
            name="test-project",
            description="A test project",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/test-project",
                ref="main",
                path="/",
            ),
        )
        config.with_notebook()

        yaml_str = render_yaml(config)

        assert "name: test-project" in yaml_str
        assert "description: A test project" in yaml_str
        assert "url: https://github.com/user/test-project" in yaml_str
        assert "ref: main" in yaml_str

    def test_stable_output(self) -> None:
        """Output should be stable across multiple renders."""
        config = LaunchableConfig(
            name="stable-test",
            description="Testing stability",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/stable-test",
                ref="main",
                path="/",
            ),
        )
        config.with_notebook()

        # Render multiple times
        yaml1 = render_yaml(config)
        yaml2 = render_yaml(config)

        # Remove timestamp line for comparison
        lines1 = [l for l in yaml1.split("\n") if "generated_at" not in l]
        lines2 = [l for l in yaml2.split("\n") if "generated_at" not in l]

        assert lines1 == lines2

    def test_notebook_config(self) -> None:
        """Should include notebook configuration."""
        config = LaunchableConfig(
            name="notebook-test",
            description="Notebook test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/notebook-test",
                ref="main",
                path="/",
            ),
        )
        config.with_notebook(
            command="jupyter lab --ip=0.0.0.0 --port=8888 --no-browser",
            port=8888,
        )

        yaml_str = render_yaml(config)

        assert "notebook:" in yaml_str
        assert "enable_jupyter: true" in yaml_str
        assert "jupyter lab" in yaml_str
        assert "8888" in yaml_str

    def test_webapp_config(self) -> None:
        """Should include webapp configuration."""
        config = LaunchableConfig(
            name="webapp-test",
            description="Webapp test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/webapp-test",
                ref="main",
                path="/",
            ),
        )
        config.with_webapp(command="python app.py", port=7860)

        yaml_str = render_yaml(config)

        assert "webapp:" in yaml_str
        assert "expose_port: 7860" in yaml_str
        assert "python app.py" in yaml_str

    def test_key_ordering(self) -> None:
        """Keys should be in logical order."""
        config = LaunchableConfig(
            name="order-test",
            description="Order test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/order-test",
                ref="main",
                path="/",
            ),
        )
        config.with_notebook()

        yaml_str = render_yaml(config)

        # Check that major sections appear in expected order
        name_pos = yaml_str.find("name:")
        desc_pos = yaml_str.find("description:")
        source_pos = yaml_str.find("source:")
        runtime_pos = yaml_str.find("runtime:")
        compute_pos = yaml_str.find("compute:")
        networking_pos = yaml_str.find("networking:")
        metadata_pos = yaml_str.find("metadata:")

        assert name_pos < desc_pos < source_pos < runtime_pos < compute_pos < networking_pos < metadata_pos

    def test_metadata_included(self) -> None:
        """Should include generation metadata."""
        config = LaunchableConfig(
            name="meta-test",
            description="Metadata test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/meta-test",
                ref="main",
                path="/",
            ),
        )

        yaml_str = render_yaml(config)

        assert "generated_by: brev-launcher" in yaml_str
        assert "generated_at:" in yaml_str


class TestWriteLaunchableYaml:
    """Tests for write_launchable_yaml function."""

    def test_writes_file(self, tmp_path: Path) -> None:
        """Should write launchable.yaml to specified directory."""
        config = LaunchableConfig(
            name="write-test",
            description="Write test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/write-test",
                ref="main",
                path="/",
            ),
        )

        output_path = write_launchable_yaml(config, tmp_path)

        assert output_path.exists()
        assert output_path.name == "launchable.yaml"
        assert "name: write-test" in output_path.read_text()

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        """Should overwrite existing launchable.yaml."""
        existing = tmp_path / "launchable.yaml"
        existing.write_text("old content")

        config = LaunchableConfig(
            name="overwrite-test",
            description="Overwrite test",
            source=SourceConfig(
                type="git",
                url="https://github.com/user/overwrite-test",
                ref="main",
                path="/",
            ),
        )

        write_launchable_yaml(config, tmp_path)

        content = existing.read_text()
        assert "old content" not in content
        assert "overwrite-test" in content

