"""Brev Launcher CLI - Generate Brev Launchable configs."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from . import __version__
from .constants import (
    DEFAULT_JUPYTER_PORT,
    DEFAULT_NOTEBOOK_COMMAND,
    DEFAULT_WEBAPP_COMMAND,
    DEFAULT_WEBAPP_PORT,
    EXIT_GENERATION_FAILURE,
    EXIT_SUCCESS,
    EXIT_VALIDATION_FAILURE,
    PROJECT_TYPE_NOTEBOOK,
    PROJECT_TYPE_WEBAPP,
)
from .detect import detect_dependency_file, detect_entry_file, estimate_vram_usage, find_candidate_entry_files
from .gitinfo import GitError
from .launchable_schema import LaunchableConfig, SourceConfig
from .output import (
    console,
    print_badge_snippet,
    print_doctor_results,
    print_error,
    print_file_written,
    print_info,
    print_next_steps,
    print_smoke_test_checklist,
    print_success,
    print_validation_error,
    print_warning,
    print_yaml_preview,
)
from .pricing import GPU_PRICING, calculate_monthly_cost, calculate_yearly_cost, recommend_gpu
from .project_scan import scan_project
from .render_yaml import render_yaml, write_launchable_yaml

app = typer.Typer(
    name="brev-launcher",
    help="Generate Brev Launchable config files from your project.",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"brev-launcher {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Brev Launcher - Generate Brev Launchable configs."""
    pass


@app.command()
def init(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Project directory path (defaults to current directory).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        "-y",
        help="Use defaults without prompting.",
    ),
    project_type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Project type: notebook or webapp.",
    ),
    port: Optional[int] = typer.Option(
        None,
        "--port",
        "-p",
        help="Port for webapp (default: 7860) or Jupyter (default: 8888).",
    ),
) -> None:
    """Initialize a Brev Launchable config for the current project.

    This command:
    1. Validates git repository setup
    2. Detects project type and dependencies
    3. Asks a few questions (unless --non-interactive)
    4. Generates launchable.yaml
    5. Prints next steps and badge snippet
    """
    console.print()
    console.print("[bold]🚀 Brev Launcher - Initialize Launchable Config[/bold]")
    console.print()

    # Step 0: Validation
    print_info("Scanning project...")

    try:
        scan = scan_project(path)
        has_git = True
    except GitError as e:
        has_git = False
        if non_interactive:
            print_validation_error(str(e))
            raise typer.Exit(EXIT_VALIDATION_FAILURE)
        
        # Ask user if they want to continue anyway (for testing in Brev)
        console.print()
        print_warning(str(e))
        console.print()
        
        if not Confirm.ask(
            "Continue anyway? (You'll need to manually add git info to the YAML)",
            default=False,
        ):
            raise typer.Exit(EXIT_VALIDATION_FAILURE)
        
        # Create a minimal scan without git
        from .project_scan import ProjectScan, check_brev_cli
        from .detect import (
            detect_dependency_file,
            detect_entry_file,
            infer_project_type,
            get_install_command,
        )
        
        dependency_file = detect_dependency_file(path)
        inferred_type = infer_project_type(path)
        
        # Create a dummy GitInfo
        from .gitinfo import GitInfo
        dummy_git = GitInfo(
            origin_url="https://github.com/YOUR_USERNAME/YOUR_REPO",
            normalized_url="https://github.com/YOUR_USERNAME/YOUR_REPO",
            default_branch="main",
            repo_name=path.name,
        )
        
        scan = ProjectScan(
            path=path,
            git=dummy_git,
            dependency_file=dependency_file,
            entry_file=detect_entry_file(path, inferred_type),
            inferred_type=inferred_type,
            install_command=get_install_command(dependency_file),
            brev=check_brev_cli(),
        )
    
    if has_git:
        print_success(f"Git repository: {scan.git.normalized_url}")
        print_success(f"Default branch: {scan.git.default_branch}")
    else:
        print_warning("Git repository: Not configured (will need manual setup)")

    if scan.dependency_file:
        print_success(f"Dependency file: {scan.dependency_file}")
    else:
        print_warning("No requirements.txt or pyproject.toml found")

    if scan.entry_file:
        print_success(f"Entry file detected: {scan.entry_file}")

    # Show Brev/GPU detection info
    if scan.brev.available:
        print_info(f"Brev CLI available (instance: {scan.brev.instance_name or 'unknown'})")
    
    if scan.brev.gpu_type and scan.brev.gpu_type != "any":
        gpu_info = f"GPU detected: {scan.brev.gpu_type}"
        if scan.brev.gpu_memory_gb:
            gpu_info += f" ({scan.brev.gpu_memory_gb}GB VRAM)"
        print_success(gpu_info)

    # Step 1: Minimal questions
    console.print()

    # Determine project type
    if project_type:
        chosen_type = project_type
    elif non_interactive:
        chosen_type = scan.inferred_type
    else:
        default_type = scan.inferred_type
        chosen_type = Prompt.ask(
            "Project type?",
            choices=[PROJECT_TYPE_NOTEBOOK, PROJECT_TYPE_WEBAPP],
            default=default_type,
        )

    # Determine port
    if port:
        chosen_port = port
    elif non_interactive:
        chosen_port = (
            DEFAULT_JUPYTER_PORT if chosen_type == PROJECT_TYPE_NOTEBOOK else DEFAULT_WEBAPP_PORT
        )
    else:
        default_port = (
            DEFAULT_JUPYTER_PORT if chosen_type == PROJECT_TYPE_NOTEBOOK else DEFAULT_WEBAPP_PORT
        )
        if chosen_type == PROJECT_TYPE_WEBAPP:
            chosen_port = IntPrompt.ask("Port?", default=default_port)
        else:
            chosen_port = default_port

    # Determine start command
    if non_interactive:
        if chosen_type == PROJECT_TYPE_NOTEBOOK:
            chosen_command = DEFAULT_NOTEBOOK_COMMAND
        else:
            chosen_command = DEFAULT_WEBAPP_COMMAND
    else:
        if chosen_type == PROJECT_TYPE_NOTEBOOK:
            default_command = DEFAULT_NOTEBOOK_COMMAND
        else:
            default_command = DEFAULT_WEBAPP_COMMAND
        chosen_command = Prompt.ask("Start command?", default=default_command)

    # Step 2: Build configuration
    console.print()
    print_info("Generating configuration...")

    try:
        config = LaunchableConfig(
            name=scan.git.repo_name,
            description=f"{scan.git.repo_name} - deployed via Brev Launchables",
            source=SourceConfig(
                type="git",
                url=scan.git.normalized_url,
                ref=scan.git.default_branch,
                path="/",
            ),
        )

        # Set install command
        config.with_install_command(scan.install_command)

        # Set GPU if detected
        if scan.brev.gpu_type and scan.brev.gpu_type != "any":
            gpu_note = f"Auto-detected from current instance"
            if scan.brev.gpu_memory_gb:
                gpu_note += f" ({scan.brev.gpu_memory_gb}GB VRAM)"
            config.with_gpu(scan.brev.gpu_type, gpu_note)
        else:
            # Use default "any" with helpful note
            config.with_gpu("any", "Select lowest-cost GPU in Brev UI")

        # Configure based on type
        if chosen_type == PROJECT_TYPE_NOTEBOOK:
            config.with_notebook(command=chosen_command, port=chosen_port)
        else:
            config.with_webapp(command=chosen_command, port=chosen_port)

        # Step 3: Write launchable.yaml
        output_path = write_launchable_yaml(config, path)
        print_file_written(output_path)

        # Show preview
        yaml_content = render_yaml(config)
        print_yaml_preview(yaml_content)

        # Step 4: Print next steps and badge
        print_next_steps(output_path)
        print_badge_snippet()
        print_smoke_test_checklist()

        console.print()
        print_success("Done! Your Launchable config is ready.")

    except typer.Exit:
        raise
    except Exception as e:
        print_error(f"Failed to generate config: {e}")
        raise typer.Exit(EXIT_GENERATION_FAILURE)


@app.command()
def doctor(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Project directory path.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """Check project health and Brev compatibility.

    Runs a series of checks to verify the project is ready for Brev deployment.
    """
    console.print()
    console.print("[bold]🩺 Brev Launcher - Project Doctor[/bold]")
    console.print()

    checks: list[tuple[str, bool, str]] = []

    # Check git repo
    from .gitinfo import is_git_repo, get_origin_url

    if is_git_repo(path):
        checks.append(("Git repository", True, "Project is a git repo"))
    else:
        checks.append(("Git repository", False, "Not a git repository"))

    # Check origin
    origin = get_origin_url(path)
    if origin:
        checks.append(("Origin remote", True, origin))
    else:
        checks.append(("Origin remote", False, "No origin remote configured"))

    # Check dependency file
    dep_file = detect_dependency_file(path)
    if dep_file:
        checks.append(("Dependencies", True, f"Found {dep_file}"))
    else:
        checks.append(("Dependencies", False, "No requirements.txt or pyproject.toml"))

    # Check entry file
    entry = detect_entry_file(path)
    if entry:
        checks.append(("Entry file", True, f"Found {entry}"))
    else:
        candidates = find_candidate_entry_files(path)
        if candidates:
            checks.append(("Entry file", True, f"Candidates: {', '.join(candidates[:3])}"))
        else:
            checks.append(("Entry file", False, "No entry file found"))

    # Check launchable.yaml
    launchable = path / "launchable.yaml"
    if launchable.exists():
        checks.append(("Launchable config", True, "launchable.yaml exists"))
    else:
        checks.append(("Launchable config", False, "Run 'brev-launcher init' to create"))

    # Check .env.example
    from .detect import detect_env_example

    if detect_env_example(path):
        checks.append(("Environment", True, ".env.example found"))
    else:
        checks.append(("Environment", True, "No .env.example (optional)"))

    print_doctor_results(checks)

    # Exit with appropriate code
    all_passed = all(passed for _, passed, _ in checks)
    raise typer.Exit(EXIT_SUCCESS if all_passed else EXIT_VALIDATION_FAILURE)


@app.command("print-badge")
def print_badge(
    launchable_id: str = typer.Argument(
        "env-REPLACE_ME",
        help="Launchable ID from Brev console.",
    ),
) -> None:
    """Print a deploy badge snippet for your README.

    Use after creating a Launchable in the Brev console.
    Get the Launchable ID from the deployment URL.
    """
    console.print()
    console.print("[bold]🏷️  Brev Launcher - Badge Generator[/bold]")
    print_badge_snippet(launchable_id)
    raise typer.Exit(EXIT_SUCCESS)


@app.command("cost-estimate")
def cost_estimate(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Project directory path (defaults to current directory).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    hours_per_day: int = typer.Option(
        24,
        "--hours",
        "-h",
        help="Expected hours of usage per day (default: 24 for always-on).",
    ),
) -> None:
    """Estimate deployment costs and recommend optimal GPU.
    
    Analyzes your project to estimate VRAM requirements and shows
    cost comparison across different GPU options.
    """
    console.print()
    console.print("[bold]💰 GPU Cost Analyzer[/bold]")
    console.print()
    
    # Try to scan project for info
    print_info("Analyzing project...")
    
    try:
        scan = scan_project(path)
        current_gpu = scan.brev.gpu_type if scan.brev.gpu_type else "gpu_1x_a10"
        has_git = True
    except GitError:
        # No git repo, use defaults
        current_gpu = "gpu_1x_a10"
        has_git = False
    
    current_info = GPU_PRICING.get(current_gpu, GPU_PRICING["gpu_1x_a10"])
    
    # Estimate VRAM usage
    estimated_vram = estimate_vram_usage(path)
    
    # Display current setup
    console.print("[bold cyan]Current Configuration:[/bold cyan]")
    console.print(f"  GPU: {current_info['name']} ({current_info['vram_gb']}GB VRAM)")
    console.print(f"  Cost: [yellow]${current_info['cost_per_hour']:.2f}/hour[/yellow]")
    console.print(f"  Monthly: [yellow]${calculate_monthly_cost(current_info['cost_per_hour'], hours_per_day):.0f}[/yellow]")
    console.print(f"  Yearly: [yellow]${calculate_yearly_cost(current_info['cost_per_hour'], hours_per_day):.0f}[/yellow]")
    console.print()
    
    if estimated_vram:
        console.print(f"[bold cyan]Estimated VRAM Requirement:[/bold cyan] {estimated_vram:.1f}GB")
        console.print("  (Based on detected models in your code)")
        console.print()
    else:
        console.print("[yellow]⚠️  Could not estimate VRAM usage from code[/yellow]")
        console.print("  Using conservative estimate of 8GB")
        estimated_vram = 8.0
        console.print()
    
    # Get recommendations
    recommendation = recommend_gpu(estimated_vram, current_gpu)
    
    # Create comparison table
    table = Table(title="💡 GPU Options Comparison", show_header=True, header_style="bold magenta")
    table.add_column("GPU", style="cyan", width=12)
    table.add_column("VRAM", justify="right", width=8)
    table.add_column("$/Hour", justify="right", width=10)
    table.add_column(f"$/Month\n({hours_per_day}h/day)", justify="right", width=12)
    table.add_column(f"$/Year\n({hours_per_day}h/day)", justify="right", width=12)
    table.add_column("vs Current", justify="right", width=15)
    table.add_column("Status", width=10)
    
    for gpu_id, info in sorted(GPU_PRICING.items(), key=lambda x: x[1]["cost_per_hour"]):
        if gpu_id == "any":
            continue
        
        monthly = calculate_monthly_cost(info["cost_per_hour"], hours_per_day)
        yearly = calculate_yearly_cost(info["cost_per_hour"], hours_per_day)
        
        current_monthly = calculate_monthly_cost(current_info["cost_per_hour"], hours_per_day)
        savings_monthly = current_monthly - monthly
        
        # Determine if GPU fits requirements
        fits = info["vram_gb"] >= estimated_vram * 0.9  # 10% tolerance
        
        # Status indicators
        if gpu_id == current_gpu:
            status = "🔵 Current"
        elif not fits:
            status = "❌ Too small"
        elif savings_monthly > 0:
            status = "✅ Cheaper"
        elif savings_monthly < 0:
            status = "⚠️ Pricier"
        else:
            status = "➖ Same"
        
        # Savings column
        if gpu_id == current_gpu:
            savings_str = "—"
        elif savings_monthly > 0:
            savings_str = f"[green]+${savings_monthly:.0f}/mo[/green]"
        elif savings_monthly < 0:
            savings_str = f"[red]-${abs(savings_monthly):.0f}/mo[/red]"
        else:
            savings_str = "±$0/mo"
        
        table.add_row(
            info["name"],
            f"{info['vram_gb']}GB",
            f"${info['cost_per_hour']:.2f}",
            f"${monthly:.0f}",
            f"${yearly:.0f}",
            savings_str,
            status,
        )
    
    console.print(table)
    console.print()
    
    # Show recommendation
    if recommendation["recommended"] and recommendation["recommended"] != current_gpu:
        rec_info = recommendation["info"]
        savings = recommendation["savings"]
        
        console.print("[bold green]💡 Recommendation:[/bold green]")
        console.print(f"  Switch to [bold]{rec_info['name']}[/bold] ({rec_info['vram_gb']}GB VRAM)")
        console.print(f"  Savings: [green]${savings['monthly']:.0f}/month[/green] or [green]${savings['yearly']:.0f}/year[/green]")
        console.print(f"  Best for: {rec_info['good_for']}")
        console.print()
    elif recommendation["recommended"] == current_gpu:
        console.print("[bold green]✅ Current GPU is optimal for your requirements![/bold green]")
        console.print()
    else:
        console.print("[yellow]⚠️  Your requirements need a larger GPU[/yellow]")
        console.print()
    
    # Usage tips
    console.print("[dim]💡 Tips:[/dim]")
    console.print("[dim]  • Run with --hours N to estimate for N hours/day usage[/dim]")
    console.print("[dim]  • Costs shown are for continuous running[/dim]")
    console.print("[dim]  • Consider stopping instances when not in use to save costs[/dim]")
    console.print()


if __name__ == "__main__":
    app()

