import os
import json
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.advai/skills")
CONFIG_DIR = os.path.expanduser("~/.advai")


def _skill_path(skill_name: str) -> str:
    return os.path.join(SKILLS_DIR, skill_name)


def _meta_path(skill_name: str) -> str:
    return os.path.join(_skill_path(skill_name), "skill.json")


def install_skill(skill_name: str, force: bool = False) -> None:
    """安装一个 Skill（当前为占位实现，后续接实际下载/配置逻辑）"""
    path = _skill_path(skill_name)
    if os.path.exists(path) and not force:
        raise FileExistsError(skill_name)

    os.makedirs(path, exist_ok=True)
    meta = {
        "name": skill_name,
        "version": "0.1.0",
        "installed_at": datetime.utcnow().isoformat() + "Z",
        "status": "installed",
    }
    with open(_meta_path(skill_name), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def uninstall_skill(skill_name: str) -> None:
    import shutil
    path = _skill_path(skill_name)
    if not os.path.exists(path):
        raise FileNotFoundError(skill_name)
    shutil.rmtree(path)


def list_skills():
    if not os.path.isdir(SKILLS_DIR):
        return []
    return sorted(
        name for name in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, name)) and not name.startswith(".")
    )


def update_skill(skill_name=None):
    """更新指定或全部已安装 Skill。当前为占位实现：只刷新元数据时间戳。"""
    targets = [skill_name] if skill_name else list_skills()
    updated = []
    for name in targets:
        if not os.path.isdir(_skill_path(name)):
            continue
        try:
            install_skill(name, force=True)
            updated.append(name)
        except Exception:
            continue
    return updated


def info_skill(skill_name: str):
    mp = _meta_path(skill_name)
    if not os.path.isfile(mp):
        sp = _skill_path(skill_name)
        if not os.path.isdir(sp):
            return None
        return {"status": "installed", "version": "unknown"}
    with open(mp, "r", encoding="utf-8") as f:
        return json.load(f)
