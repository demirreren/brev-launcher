"""Tests for gitinfo module."""

import pytest

from brev_launcher.gitinfo import extract_repo_name, normalize_git_url


class TestNormalizeGitUrl:
    """Tests for normalize_git_url function."""

    def test_ssh_to_https(self) -> None:
        """Should convert SSH URL to HTTPS."""
        url = "git@github.com:user/repo.git"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/user/repo"

    def test_ssh_without_git_suffix(self) -> None:
        """Should handle SSH URL without .git suffix."""
        url = "git@github.com:user/repo"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/user/repo"

    def test_https_with_git_suffix(self) -> None:
        """Should remove .git suffix from HTTPS URL."""
        url = "https://github.com/user/repo.git"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/user/repo"

    def test_https_already_clean(self) -> None:
        """Should preserve clean HTTPS URL."""
        url = "https://github.com/user/repo"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/user/repo"

    def test_git_protocol(self) -> None:
        """Should convert git:// protocol to HTTPS."""
        url = "git://github.com/user/repo.git"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/user/repo"

    def test_gitlab_ssh(self) -> None:
        """Should work with GitLab SSH URLs."""
        url = "git@gitlab.com:user/repo.git"
        normalized = normalize_git_url(url)
        assert normalized == "https://gitlab.com/user/repo"

    def test_nested_path(self) -> None:
        """Should handle nested paths."""
        url = "git@github.com:org/team/repo.git"
        normalized = normalize_git_url(url)
        assert normalized == "https://github.com/org/team/repo"


class TestExtractRepoName:
    """Tests for extract_repo_name function."""

    def test_https_url(self) -> None:
        """Should extract repo name from HTTPS URL."""
        url = "https://github.com/user/my-project"
        name = extract_repo_name(url)
        assert name == "my-project"

    def test_https_url_with_git(self) -> None:
        """Should extract repo name and strip .git."""
        url = "https://github.com/user/my-project.git"
        name = extract_repo_name(url)
        assert name == "my-project"

    def test_ssh_url(self) -> None:
        """Should extract repo name from SSH URL."""
        url = "git@github.com:user/awesome-repo.git"
        name = extract_repo_name(url)
        assert name == "awesome-repo"

    def test_trailing_slash(self) -> None:
        """Should handle trailing slash."""
        url = "https://github.com/user/repo/"
        name = extract_repo_name(url)
        assert name == "repo"

