#!/usr/bin/env node
/**
 * npm postinstall 时自检 Python 是否可用；不可用时只打印提示，不阻塞安装。
 */
const { spawnSync } = require("child_process");
const r = spawnSync("python3", ["--version"], { stdio: "pipe" });
if (r.status !== 0 && r.status !== 1) {
  process.stdout.write(
    "[advai] 检测到未安装 Python 3。advai 命令需要 Python 3 才能运行。\n" +
      "        请访问 https://www.python.org/downloads/ 安装后再使用 `advai`。\n"
  );
}
