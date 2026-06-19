#!/usr/bin/env node
/**
 * advai — Node.js 入口包装器
 * npm install -g advai 后，`advai` 命令最终通过此脚本桥接到 Python 核心。
 *
 * 设计：
 *  1) 优先使用系统 python3 直接调用随包附带的 advai/cli.py；
 *  2) 若当前环境通过 pip 已安装同名 advai Python 包，则走 entry-point；
 *  3) 找不到 python3 时给出友好提示。
 */
const { spawn, spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

// ---- locate python3 ----
function findPython() {
  const candidates = ["python3", "python"];
  for (const exe of candidates) {
    const r = spawnSync(exe, ["--version"], { stdio: "ignore" });
    if (r.status === 0 || r.status === 1) return exe;
  }
  return null;
}

// ---- locate advai/cli.py inside this npm package ----
function findLocalCli() {
  const candidate = path.resolve(__dirname, "..", "advai", "cli.py");
  if (fs.existsSync(candidate)) return candidate;
  return null;
}

const python = findPython();
if (!python) {
  process.stderr.write(
    "advai 需要 Python 3，请先安装 Python 3：https://www.python.org/downloads/\n"
  );
  process.exit(2);
}

const localCli = findLocalCli();
const argv = process.argv.slice(2);

let child;
if (localCli) {
  // 直接用当前 npm 包内的 Python 源码运行（无需额外 pip install）
  child = spawn(python, [localCli, ...argv], { stdio: "inherit" });
} else {
  // 回退：假设用户已通过 pip 安装了同名 advai 包，走 entry-point
  child = spawn(python, ["-m", "advai", ...argv], { stdio: "inherit" });
}

child.on("exit", (code) => process.exit(code === null ? 1 : code));
child.on("error", (err) => {
  process.stderr.write("无法启动 advai: " + err.message + "\n");
  process.exit(1);
});
