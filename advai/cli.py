import click
import os
import sys
import json

from advai.skills import install_skill, uninstall_skill, list_skills, update_skill, info_skill

SKILLS_DIR = os.path.expanduser("~/.advai/skills")
CONFIG_DIR = os.path.expanduser("~/.advai")


def _ensure_dirs():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)


@click.group()
@click.version_option(package_name="advai")
def cli():
    """advai — 跨平台 AI Skill 管理器"""
    _ensure_dirs()


@cli.command()
@click.argument("skill_name")
@click.option("--force", is_flag=True, help="强制重新安装（覆盖已有版本）")
def install(skill_name, force):
    """安装一个 Skill: advai install <skill-name>"""
    try:
        install_skill(skill_name, force=force)
        click.echo(f"✅ Skill '{skill_name}' 安装成功")
    except FileExistsError:
        click.echo(f"⚠️  Skill '{skill_name}' 已经存在，使用 --force 可覆盖")
    except Exception as e:
        click.echo(f"❌ 安装失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("skill_name")
def uninstall(skill_name):
    """卸载一个 Skill: advai uninstall <skill-name>"""
    try:
        uninstall_skill(skill_name)
        click.echo(f"🗑️  Skill '{skill_name}' 已卸载")
    except FileNotFoundError:
        click.echo(f"⚠️  Skill '{skill_name}' 未安装")
    except Exception as e:
        click.echo(f"❌ 卸载失败: {e}", err=True)
        sys.exit(1)


@cli.command(name="list")
def list_cmd():
    """列出本地已安装的 Skills"""
    skills = list_skills()
    if not skills:
        click.echo("(暂无已安装的 Skill)")
        return
    click.echo("📋 已安装 Skills:")
    for s in skills:
        click.echo(f"  • {s}")


@cli.command()
@click.argument("skill_name", required=False)
def update(skill_name):
    """更新一个（或全部）Skill: advai update [skill-name]"""
    try:
        updated = update_skill(skill_name)
        if updated:
            for s in updated:
                click.echo(f"🔄 {s} 已更新")
        else:
            click.echo("(没有可更新的 Skill)")
    except Exception as e:
        click.echo(f"❌ 更新失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("skill_name")
def info(skill_name):
    """查看 Skill 详情: advai info <skill-name>"""
    data = info_skill(skill_name)
    if data is None:
        click.echo(f"⚠️  Skill '{skill_name}' 未安装或无元数据")
        return
    click.echo(f"ℹ️  Skill '{skill_name}':")
    for k, v in data.items():
        click.echo(f"  {k}: {v}")


if __name__ == "__main__":
    cli()
