#!/usr/bin/env node
/**
 * Post-install sanity check — verifies Python 3 is available on the system.
 * Prints a friendly hint if missing, but never blocks installation.
 */
const { spawnSync } = require("child_process");
const r = spawnSync("python3", ["--version"], { stdio: "pipe" });
if (r.status !== 0 && r.status !== 1) {
  process.stdout.write(
    "[advai] Python 3 was not detected. The `advai` command requires Python 3 to run.\n" +
      "        Please install it from https://www.python.org/downloads/ and then run `advai`.\n"
  );
}
