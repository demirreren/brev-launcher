"""Tests for detect module."""

import tempfile
from pathlib import Path

import pytest

from brev_launcher.detect import (
    detect_dependency_file,
    detect_entry_file,
    detect_env_example,
    detect_notebooks_folder,
    detect_ports_in_code,
    find_candidate_entry_files,
    get_install_command,
    infer_project_type,
)


class TestDetectDependencyFile:
    """Tests for detect_dependency_file."""

    def test_requirements_txt(self, tmp_path: Path) -> None:
        """Should detect requirements.txt."""
        (tmp_path / "requirements.txt").write_text("numpy==1.24.0\n")
        assert detect_dependency_file(tmp_path) == "requirements.txt"

    def test_pyproject_toml(self, tmp_path: Path) -> None:
        """Should detect pyproject.toml when no requirements.txt."""
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"\n')
        assert detect_dependency_file(tmp_path) == "pyproject.toml"

    def test_requirements_preferred_over_pyproject(self, tmp_path: Path) -> None:
        """Should prefer requirements.txt over pyproject.toml."""
        (tmp_path / "requirements.txt").write_text("numpy\n")
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"\n')
        assert detect_dependency_file(tmp_path) == "requirements.txt"

    def test_no_dependency_file(self, tmp_path: Path) -> None:
        """Should return None when no dependency file."""
        assert detect_dependency_file(tmp_path) is None


class TestDetectEntryFile:
    """Tests for detect_entry_file."""

    def test_main_ipynb_notebook(self, tmp_path: Path) -> None:
        """Should detect main.ipynb for notebook projects."""
        (tmp_path / "main.ipynb").write_text("{}")
        assert detect_entry_file(tmp_path, "notebook") == "main.ipynb"

    def test_notebook_ipynb(self, tmp_path: Path) -> None:
        """Should detect notebook.ipynb."""
        (tmp_path / "notebook.ipynb").write_text("{}")
        assert detect_entry_file(tmp_path, "notebook") == "notebook.ipynb"

    def test_any_ipynb_fallback(self, tmp_path: Path) -> None:
        """Should fall back to any .ipynb file."""
        (tmp_path / "custom.ipynb").write_text("{}")
        assert detect_entry_file(tmp_path, "notebook") == "custom.ipynb"

    def test_app_py_webapp(self, tmp_path: Path) -> None:
        """Should detect app.py for webapp projects."""
        (tmp_path / "app.py").write_text("# app")
        assert detect_entry_file(tmp_path, "webapp") == "app.py"

    def test_main_py_webapp(self, tmp_path: Path) -> None:
        """Should detect main.py for webapp projects."""
        (tmp_path / "main.py").write_text("# main")
        assert detect_entry_file(tmp_path, "webapp") == "main.py"

    def test_no_entry_file(self, tmp_path: Path) -> None:
        """Should return None when no entry file found."""
        assert detect_entry_file(tmp_path, "notebook") is None


class TestFindCandidateEntryFiles:
    """Tests for find_candidate_entry_files."""

    def test_finds_notebooks_and_py(self, tmp_path: Path) -> None:
        """Should find both notebook and Python files."""
        (tmp_path / "main.ipynb").write_text("{}")
        (tmp_path / "app.py").write_text("# app")
        (tmp_path / "utils.py").write_text("# utils")

        candidates = find_candidate_entry_files(tmp_path)
        assert "main.ipynb" in candidates
        assert "app.py" in candidates
        assert "utils.py" in candidates

    def test_excludes_test_files(self, tmp_path: Path) -> None:
        """Should exclude test files."""
        (tmp_path / "test_main.py").write_text("# test")
        (tmp_path / "app.py").write_text("# app")

        candidates = find_candidate_entry_files(tmp_path)
        assert "test_main.py" not in candidates
        assert "app.py" in candidates

    def test_excludes_init(self, tmp_path: Path) -> None:
        """Should exclude __init__.py."""
        (tmp_path / "__init__.py").write_text("")
        (tmp_path / "app.py").write_text("# app")

        candidates = find_candidate_entry_files(tmp_path)
        assert "__init__.py" not in candidates


class TestDetectEnvExample:
    """Tests for detect_env_example."""

    def test_env_example_exists(self, tmp_path: Path) -> None:
        """Should return True when .env.example exists."""
        (tmp_path / ".env.example").write_text("API_KEY=\n")
        assert detect_env_example(tmp_path) is True

    def test_no_env_example(self, tmp_path: Path) -> None:
        """Should return False when no .env.example."""
        assert detect_env_example(tmp_path) is False


class TestDetectNotebooksFolder:
    """Tests for detect_notebooks_folder."""

    def test_notebooks_folder_exists(self, tmp_path: Path) -> None:
        """Should return True when notebooks folder exists."""
        (tmp_path / "notebooks").mkdir()
        assert detect_notebooks_folder(tmp_path) is True

    def test_no_notebooks_folder(self, tmp_path: Path) -> None:
        """Should return False when no notebooks folder."""
        assert detect_notebooks_folder(tmp_path) is False

    def test_notebooks_is_file(self, tmp_path: Path) -> None:
        """Should return False when notebooks is a file."""
        (tmp_path / "notebooks").write_text("")
        assert detect_notebooks_folder(tmp_path) is False


class TestDetectPortsInCode:
    """Tests for detect_ports_in_code."""

    def test_detects_gradio_port(self, tmp_path: Path) -> None:
        """Should detect Gradio default port."""
        (tmp_path / "app.py").write_text('demo.launch(port=7860)')
        ports = detect_ports_in_code(tmp_path)
        assert 7860 in ports

    def test_detects_flask_port(self, tmp_path: Path) -> None:
        """Should detect Flask port."""
        (tmp_path / "app.py").write_text('app.run(port=5000)')
        ports = detect_ports_in_code(tmp_path)
        assert 5000 in ports

    def test_ignores_uncommon_ports(self, tmp_path: Path) -> None:
        """Should ignore uncommon ports."""
        (tmp_path / "app.py").write_text('port = 12345')
        ports = detect_ports_in_code(tmp_path)
        assert 12345 not in ports


class TestGetInstallCommand:
    """Tests for get_install_command."""

    def test_requirements_txt(self) -> None:
        """Should return pip install -r for requirements.txt."""
        cmd = get_install_command("requirements.txt")
        assert cmd == "pip install -r requirements.txt"

    def test_pyproject_toml(self) -> None:
        """Should return pip install . for pyproject.toml."""
        cmd = get_install_command("pyproject.toml")
        assert cmd == "pip install ."

    def test_none(self) -> None:
        """Should return comment for None."""
        cmd = get_install_command(None)
        assert "No dependency file found" in cmd


class TestInferProjectType:
    """Tests for infer_project_type."""

    def test_notebook_when_ipynb_present(self, tmp_path: Path) -> None:
        """Should infer notebook when .ipynb files present."""
        (tmp_path / "main.ipynb").write_text("{}")
        assert infer_project_type(tmp_path) == "notebook"

    def test_webapp_when_app_py_present(self, tmp_path: Path) -> None:
        """Should infer webapp when app.py present."""
        (tmp_path / "app.py").write_text("# app")
        assert infer_project_type(tmp_path) == "webapp"

    def test_defaults_to_notebook(self, tmp_path: Path) -> None:
        """Should default to notebook when no files."""
        assert infer_project_type(tmp_path) == "notebook"

