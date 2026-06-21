#!/usr/bin/env node
/**
 * advai — Node.js entry point.
 * After `npm install -g advai-cli`, the `advai` command routes
 * through this script to the Python core.
 *
 * Design:
 *   1) Look for python3 on the system and run advai/cli.py bundled
 *      inside this npm package.
 *   2) Fall back to `python3 -m advai` if the bundled source is not found.
 *   3) Print a friendly hint if python3 cannot be found.
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
    "advai requires Python 3. Please install Python 3 from https://www.python.org/downloads/\n"
  );
  process.exit(2);
}

const localCli = findLocalCli();
const argv = process.argv.slice(2);

let child;
if (localCli) {
  // Run directly from the bundled Python source (no additional pip install needed)
  child = spawn(python, [localCli, ...argv], { stdio: "inherit" });
} else {
  // Fallback: assume the user already installed advai via pip, use the entry point
  child = spawn(python, ["-m", "advai", ...argv], { stdio: "inherit" });
}

child.on("exit", (code) => process.exit(code === null ? 1 : code));
child.on("error", (err) => {
  process.stderr.write("Failed to start advai: " + err.message + "\n");
  process.exit(1);
});
