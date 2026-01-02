"""Terminal output formatting."""

from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from .constants import BREV_DEPLOY_BADGE_URL, BREV_DEPLOY_URL_TEMPLATE

console = Console()


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]✗[/bold red] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[bold yellow]![/bold yellow] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold blue]→[/bold blue] {message}")


def print_file_written(file_path: Path) -> None:
    """Print file written confirmation."""
    print_success(f"Created [bold]{file_path}[/bold]")


def print_validation_error(message: str) -> None:
    """Print a validation error with formatting."""
    console.print()
    console.print(Panel(message, title="[red]Validation Error[/red]", border_style="red"))


def print_next_steps(launchable_path: Path) -> None:
    """Print the next steps after generating launchable.yaml."""
    console.print()
    console.print("[bold cyan]━━━ Next Steps ━━━[/bold cyan]")
    console.print()

    steps = """\
1. **Commit and push** `launchable.yaml` to your repository

2. **Create a Launchable** in Brev:
   - Go to [Brev Console](https://brev.nvidia.com)
   - Navigate to **Launchables** → **Create Launchable**
   - Select **Git Repository**
   - Click **Show configuration**
   - Paste the contents of `launchable.yaml`

3. **Deploy** your Launchable to a GPU instance

4. **Verify** your notebook opens or app responds
"""
    console.print(Markdown(steps))


def print_badge_snippet(launchable_id: str = "env-REPLACE_ME") -> None:
    """Print the badge snippet for README."""
    deploy_url = BREV_DEPLOY_URL_TEMPLATE.format(launchable_id=launchable_id)

    badge_markdown = f"""\
[![Deploy on Brev]({BREV_DEPLOY_BADGE_URL})]({deploy_url})
"""

    badge_html = f"""\
<a href="{deploy_url}">
  <img src="{BREV_DEPLOY_BADGE_URL}" alt="Deploy on Brev" />
</a>
"""

    console.print()
    console.print("[bold cyan]━━━ Badge Snippet ━━━[/bold cyan]")
    console.print()
    console.print("Add this to your README to let users deploy with one click:")
    console.print()

    console.print("[bold]Markdown:[/bold]")
    console.print(Syntax(badge_markdown.strip(), "markdown", theme="monokai"))
    console.print()

    console.print("[bold]HTML:[/bold]")
    console.print(Syntax(badge_html.strip(), "html", theme="monokai"))
    console.print()

    console.print(
        f"[dim]Replace [bold]env-REPLACE_ME[/bold] with your actual Launchable ID "
        f"after creating it in the Brev console.[/dim]"
    )


def print_smoke_test_checklist() -> None:
    """Print the smoke test checklist."""
    console.print()
    console.print("[bold cyan]━━━ Smoke Test Checklist ━━━[/bold cyan]")
    console.print()

    checklist = """\
- [ ] Create Launchable from config in Brev console
- [ ] Deploy to a fresh GPU instance
- [ ] Confirm notebook opens or app responds
- [ ] Test GPU access (run `torch.cuda.is_available()`)
"""
    console.print(Markdown(checklist))


def print_doctor_results(checks: list[tuple[str, bool, str]]) -> None:
    """Print doctor command results.

    Args:
        checks: List of (check_name, passed, message) tuples.
    """
    console.print()
    console.print("[bold cyan]━━━ Project Health Check ━━━[/bold cyan]")
    console.print()

    all_passed = True
    for name, passed, message in checks:
        if passed:
            console.print(f"[green]✓[/green] {name}: {message}")
        else:
            console.print(f"[red]✗[/red] {name}: {message}")
            all_passed = False

    console.print()
    if all_passed:
        print_success("All checks passed!")
    else:
        print_warning("Some checks failed. See above for details.")


def print_yaml_preview(yaml_content: str, max_lines: int = 50) -> None:
    """Print a preview of the YAML content."""
    lines = yaml_content.split("\n")
    if len(lines) > max_lines:
        preview = "\n".join(lines[:max_lines]) + "\n# ... (truncated)"
    else:
        preview = yaml_content

    console.print()
    console.print("[bold]Generated launchable.yaml:[/bold]")
    console.print(Syntax(preview, "yaml", theme="monokai"))

