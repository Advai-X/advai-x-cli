import click
import os
import sys

from advai import __version__
from advai.cli_manager import (
    cli_info,
    list_available_clis,
    cli_exists,
    build_cli_exec_command,
    opencli_available,
    ensure_manager_available,
    resolve_manager,
    build_install_command,
    build_uninstall_command,
    build_update_command,
    run_manager_command,
    run_passthrough_command,
)
from advai.skills import install_skill, uninstall_skill, list_skills, update_skill, info_skill

SKILLS_DIR = os.path.expanduser("~/.advai/skills")
CONFIG_DIR = os.path.expanduser("~/.advai")


def _ensure_dirs():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)


@click.group()
@click.version_option(version=__version__, prog_name="advai")
def cli():
    """advai — a cross-platform CLI tool."""
    _ensure_dirs()


class ExternalCLIGroup(click.Group):
    """Static management commands + dynamic OpenCLI proxy."""

    def get_command(self, ctx, cmd_name):
        command = super().get_command(ctx, cmd_name)
        if command is not None:
            return command
        if not opencli_available():
            return None
        if not cli_exists(cmd_name):
            return None

        @click.command(
            name=cmd_name,
            context_settings={
                "ignore_unknown_options": True,
                "allow_extra_args": True,
            },
            add_help_option=False,
        )
        @click.argument("args", nargs=-1, type=click.UNPROCESSED)
        def dynamic_cli_cmd(args):
            exit_code = run_passthrough_command(build_cli_exec_command(cmd_name, list(args)))
            raise click.exceptions.Exit(exit_code)

        return dynamic_cli_cmd


def _skill_install(skill_name, force):
    try:
        install_skill(skill_name, force=force)
        click.echo(f"✅ Skill '{skill_name}' installed successfully")
    except FileExistsError:
        click.echo(f"⚠️  Skill '{skill_name}' already exists, use --force to overwrite")
    except Exception as e:
        click.echo(f"❌ Installation failed: {e}", err=True)
        sys.exit(1)


def _skill_uninstall(skill_name):
    try:
        uninstall_skill(skill_name)
        click.echo(f"🗑️  Skill '{skill_name}' uninstalled")
    except FileNotFoundError:
        click.echo(f"⚠️  Skill '{skill_name}' is not installed")
    except Exception as e:
        click.echo(f"❌ Uninstall failed: {e}", err=True)
        sys.exit(1)


def _skill_list():
    skills = list_skills()
    if not skills:
        click.echo("(no Skills installed)")
        return
    click.echo("📋 Installed Skills:")
    for s in skills:
        click.echo(f"  • {s}")


def _skill_update(skill_name):
    try:
        updated = update_skill(skill_name)
        if updated:
            for s in updated:
                click.echo(f"🔄 {s} updated")
        else:
            click.echo("(nothing to update)")
    except Exception as e:
        click.echo(f"❌ Update failed: {e}", err=True)
        sys.exit(1)


def _skill_info(skill_name):
    data = info_skill(skill_name)
    if data is None:
        click.echo(f"⚠️  Skill '{skill_name}' not installed or has no metadata")
        return
    click.echo(f"ℹ️  Skill '{skill_name}':")
    for k, v in data.items():
        click.echo(f"  {k}: {v}")


@cli.group(name="skill")
def skill_admin():
    """Manage Skills with a structured command group."""


@skill_admin.command(name="install")
@click.argument("skill_name")
@click.option("--force", is_flag=True, help="Force reinstall (overwrite existing)")
def skill_install_cmd(skill_name, force):
    """Install a Skill."""
    _skill_install(skill_name, force)


@skill_admin.command(name="uninstall")
@click.argument("skill_name")
def skill_uninstall_cmd(skill_name):
    """Uninstall a Skill."""
    _skill_uninstall(skill_name)


@skill_admin.command(name="list")
def skill_list_cmd():
    """List locally installed Skills."""
    _skill_list()


@skill_admin.command(name="update")
@click.argument("skill_name", required=False)
def skill_update_cmd(skill_name):
    """Update one or all Skills."""
    _skill_update(skill_name)


@skill_admin.command(name="info")
@click.argument("skill_name")
def skill_info_cmd(skill_name):
    """Show Skill details."""
    _skill_info(skill_name)


@cli.group(name="cli", cls=ExternalCLIGroup)
def cli_admin():
    """Manage advai itself or execute external CLIs."""


@cli_admin.command(name="info")
def cli_info_cmd():
    """Show advai CLI details."""
    data = cli_info()
    click.echo("advai CLI:")
    click.echo(f"  name: {data['name']}")
    click.echo(f"  version: {data['version']}")
    click.echo(f"  install_method: {data['install_method']}")
    click.echo(f"  python: {data['python']}")
    click.echo(f"  entry: {data['entry']}")
    click.echo(f"  module: {data['module']}")
    click.echo(f"  skills_dir: {data['skills_dir']}")
    click.echo("  available_managers:")
    for manager, available in data["available_managers"].items():
        click.echo(f"    {manager}: {'yes' if available else 'no'}")


@cli_admin.command(name="list")
@click.option("--search", default="", help="Filter CLI names")
def cli_list_cmd(search):
    """List executable external CLIs."""
    if not opencli_available():
        raise click.ClickException("opencli is not installed or not on PATH")
    targets = list_available_clis(search)
    if not targets:
        click.echo("(no external CLIs found)")
        return
    click.echo("Executable CLIs:")
    for item in targets:
        preview = ", ".join(item["commands"][:5])
        if item["command_count"] > 5:
            preview += ", ..."
        click.echo(f"  • {item['name']} ({item['command_count']} commands)")
        if preview:
            click.echo(f"    commands: {preview}")


def _execute_cli_command(command, action):
    result = run_manager_command(command)
    if result["stdout"]:
        click.echo(result["stdout"])
    if result["returncode"] != 0:
        if result["stderr"]:
            click.echo(result["stderr"], err=True)
        raise click.ClickException(f"CLI {action} failed")
    if result["stderr"]:
        click.echo(result["stderr"])


@cli_admin.command(name="install")
@click.option("--manager", type=click.Choice(["pip", "npm", "brew"]), help="Package manager to use")
@click.option("--reinstall", is_flag=True, help="Force reinstall where supported")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
def cli_install_cmd(manager, reinstall, yes):
    """Install or reinstall the advai CLI."""
    manager = resolve_manager(manager)
    ensure_manager_available(manager)
    command = build_install_command(manager, reinstall=reinstall)
    if not yes:
        click.confirm(f"Run install via {manager}: {' '.join(command)} ?", abort=True)
    _execute_cli_command(command, "install")
    click.echo(f"CLI install completed via {manager}")


@cli_admin.command(name="update")
@click.option("--manager", type=click.Choice(["pip", "npm", "brew"]), help="Package manager to use")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
def cli_update_cmd(manager, yes):
    """Update the advai CLI."""
    manager = resolve_manager(manager)
    ensure_manager_available(manager)
    command = build_update_command(manager)
    if not yes:
        click.confirm(f"Run update via {manager}: {' '.join(command)} ?", abort=True)
    _execute_cli_command(command, "update")
    click.echo(f"CLI update completed via {manager}")


@cli_admin.command(name="uninstall")
@click.option("--manager", type=click.Choice(["pip", "npm", "brew"]), help="Package manager to use")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
def cli_uninstall_cmd(manager, yes):
    """Uninstall the advai CLI."""
    manager = resolve_manager(manager)
    ensure_manager_available(manager)
    command = build_uninstall_command(manager)
    if not yes:
        click.confirm(f"Run uninstall via {manager}: {' '.join(command)} ?", abort=True)
    _execute_cli_command(command, "uninstall")
    click.echo(f"CLI uninstall completed via {manager}")


if __name__ == "__main__":
    cli()
