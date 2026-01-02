"""Git information extraction and URL normalization."""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class GitInfo:
    """Git repository information."""

    origin_url: str
    normalized_url: str
    default_branch: str
    repo_name: str


class GitError(Exception):
    """Git-related error."""

    pass


def is_git_repo(path: Path = Path.cwd()) -> bool:
    """Check if the given path is inside a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_origin_url(path: Path = Path.cwd()) -> Optional[str]:
    """Get the origin remote URL."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def normalize_git_url(url: str) -> str:
    """Normalize a git URL to HTTPS GitHub format.

    Handles:
    - git@github.com:user/repo.git -> https://github.com/user/repo
    - https://github.com/user/repo.git -> https://github.com/user/repo
    - git://github.com/user/repo.git -> https://github.com/user/repo
    """
    # Remove trailing .git
    url = re.sub(r"\.git$", "", url)

    # SSH format: git@github.com:user/repo
    ssh_match = re.match(r"git@([^:]+):(.+)", url)
    if ssh_match:
        host, path = ssh_match.groups()
        return f"https://{host}/{path}"

    # Git protocol: git://github.com/user/repo
    git_match = re.match(r"git://([^/]+)/(.+)", url)
    if git_match:
        host, path = git_match.groups()
        return f"https://{host}/{path}"

    # Already HTTPS or HTTP
    if url.startswith("http://") or url.startswith("https://"):
        return url

    return url


def get_default_branch(path: Path = Path.cwd()) -> str:
    """Get the default branch name."""
    # Try to get from remote HEAD
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            # refs/remotes/origin/main -> main
            ref = result.stdout.strip()
            return ref.split("/")[-1]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: check if main or master exists
    for branch in ["main", "master"]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--verify", f"refs/heads/{branch}"],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return branch
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return "main"


def extract_repo_name(url: str) -> str:
    """Extract repository name from URL."""
    # Remove .git suffix
    url = re.sub(r"\.git$", "", url)

    # Get last path component
    parts = url.rstrip("/").split("/")
    return parts[-1] if parts else "project"


def get_git_info(path: Path = Path.cwd()) -> GitInfo:
    """Get complete git information for the repository.

    Raises:
        GitError: If not a git repo or origin is missing.
    """
    if not is_git_repo(path):
        raise GitError(
            "Not a git repository.\n\n"
            "Fix: Initialize a git repository:\n"
            "  git init\n"
            "  git add .\n"
            "  git commit -m 'Initial commit'\n"
            "  git remote add origin <your-repo-url>"
        )

    origin_url = get_origin_url(path)
    if not origin_url:
        raise GitError(
            "No 'origin' remote found.\n\n"
            "Fix: Add an origin remote:\n"
            "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO\n\n"
            "Make sure the repository is public for Brev to access it."
        )

    normalized_url = normalize_git_url(origin_url)
    default_branch = get_default_branch(path)
    repo_name = extract_repo_name(origin_url)

    return GitInfo(
        origin_url=origin_url,
        normalized_url=normalized_url,
        default_branch=default_branch,
        repo_name=repo_name,
    )

