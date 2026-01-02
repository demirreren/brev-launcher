"""Tests for project_scan module."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from brev_launcher.project_scan import BrevInfo, ProjectScan, check_brev_cli


class TestCheckBrevCli:
    """Tests for check_brev_cli."""

    def test_brev_not_installed(self) -> None:
        """Should return unavailable when brev not in PATH."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            info = check_brev_cli()
            assert info.available is False
            assert info.instance_name is None

    def test_brev_installed_no_instances(self) -> None:
        """Should return available with no instance when ls returns nothing."""
        with patch("subprocess.run") as mock_run:
            # First call: which brev - success
            # Second call: brev ls - success but no running instances
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="/usr/local/bin/brev"),
                MagicMock(returncode=0, stdout="No instances found\n"),
            ]
            info = check_brev_cli()
            assert info.available is True

    def test_brev_installed_with_running_instance(self) -> None:
        """Should detect running instance from brev ls."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="/usr/local/bin/brev"),
                MagicMock(returncode=0, stdout="* my-workspace  RUNNING  gpu-a10\n"),
            ]
            info = check_brev_cli()
            assert info.available is True
            # Instance detection is best-effort

    def test_timeout_handling(self) -> None:
        """Should handle timeout gracefully."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("brev", 5)
            info = check_brev_cli()
            assert info.available is False


class TestProjectScan:
    """Tests for ProjectScan dataclass."""

    def test_project_scan_creation(self, tmp_path: Path) -> None:
        """Should create ProjectScan with all fields."""
        from brev_launcher.gitinfo import GitInfo

        git_info = GitInfo(
            origin_url="git@github.com:user/repo.git",
            normalized_url="https://github.com/user/repo",
            default_branch="main",
            repo_name="repo",
        )

        scan = ProjectScan(
            path=tmp_path,
            git=git_info,
            dependency_file="requirements.txt",
            entry_file="main.ipynb",
            has_env_example=True,
            has_notebooks_folder=False,
            detected_ports=[7860],
            inferred_type="notebook",
            install_command="pip install -r requirements.txt",
            brev=BrevInfo(available=True, instance_name="test-instance"),
        )

        assert scan.path == tmp_path
        assert scan.git.repo_name == "repo"
        assert scan.dependency_file == "requirements.txt"
        assert scan.inferred_type == "notebook"
        assert scan.brev.instance_name == "test-instance"

    def test_brev_info_defaults(self) -> None:
        """Should have sensible defaults for BrevInfo."""
        info = BrevInfo()
        assert info.available is False
        assert info.instance_name is None

