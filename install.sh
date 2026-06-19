#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# advai — 一键安装脚本（Mac / Linux 通用）
# 使用：
#     curl -fsSL https://raw.githubusercontent.com/Advai-X/advai-x-cli/main/install.sh | bash
# 或：
#     wget -qO- https://raw.githubusercontent.com/Advai-X/advai-x-cli/main/install.sh | bash
#
# 工作方式：
#   1. 检查是否有 python3 / pip3；没有则给出安装提示后退出
#   2. 用 pip3 install --user advai 安装核心（若环境不支持 --user，则退化为全局安装）
#   3. 将 ~/.local/bin 加入 PATH（如不在其中）
# ---------------------------------------------------------------------------

set -e

ADVAI_VERSION="${ADVAI_VERSION:-latest}"
PY="python3"
PIP="pip3"

log()  { printf "\033[1;36m[advai]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[advai][warn]\033[0m %s\n" "$*"; }
err()  { printf "\033[1;31m[advai][error]\033[0m %s\n" "$*" >&2; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

# ---- 1. 检测 Python / pip ----
if ! command_exists "$PY"; then
  err "未找到 python3，请先安装 Python 3：https://www.python.org/downloads/"
  exit 1
fi
if ! command_exists "$PIP"; then
  err "未找到 pip3，尝试用系统包管理器安装（如 apt install python3-pip / brew install python）"
  exit 1
fi

log "检测到 $(${PY} --version 2>&1 | head -n1)"

# ---- 2. 安装 advai ----
log "正在安装 advai ($ADVAI_VERSION) ..."

INSTALL_TARGET="advai"
if [ "$ADVAI_VERSION" != "latest" ]; then
  INSTALL_TARGET="advai==${ADVAI_VERSION}"
fi

# 优先 --user；若在虚拟环境中（VIRTUAL_ENV 非空），则不带 --user
if [ -n "${VIRTUAL_ENV:-}" ]; then
  "$PIP" install --upgrade "$INSTALL_TARGET"
else
  if ! "$PIP" install --user --upgrade "$INSTALL_TARGET"; then
    warn "user-site 安装失败，尝试全局安装（可能需要 sudo）"
    if [ "$(id -u)" -eq 0 ]; then
      "$PIP" install --upgrade "$INSTALL_TARGET"
    else
      sudo "$PIP" install --upgrade "$INSTALL_TARGET"
    fi
  fi
fi

# ---- 3. 确保 ~/.local/bin 在 PATH ----
LOCAL_BIN="$HOME/.local/bin"
SHELL_NAME="$(basename "${SHELL:-/bin/sh}")"
RC_FILE=""
case "$SHELL_NAME" in
  bash) RC_FILE="$HOME/.bashrc" ;;
  zsh)  RC_FILE="$HOME/.zshrc"  ;;
  fish) RC_FILE="$HOME/.config/fish/config.fish" ;;
  *)    RC_FILE="$HOME/.profile" ;;
esac

case ":$PATH:" in
  *":$LOCAL_BIN:"*) : ;;
  *)
    log "将 $LOCAL_BIN 加入 PATH（写入 $RC_FILE）"
    mkdir -p "$(dirname "$RC_FILE")"
    if [ "$SHELL_NAME" = "fish" ]; then
      echo "fish_add_path -g $LOCAL_BIN" >> "$RC_FILE"
    else
      echo "export PATH=\"$LOCAL_BIN:\$PATH\" # added by advai installer" >> "$RC_FILE"
    fi
    warn "请重新打开终端，或执行：source $RC_FILE"
    ;;
esac

log "安装完成！试试运行："
log "  advai --help"
log "  advai install <skill-name>"
