# advai-cli — Cross-platform AI Skill Manager

A Python CLI that lets you install / uninstall AI Skills like software packages.

- **Platforms**: macOS / Linux / Windows
- **Installation**: choose from `pip`, `npm`, `brew`, or `curl | bash`
- **Commands**: `install`, `uninstall`, `list`, `update`, `info`

---

## Quick Start

```bash
# Option 1: pip (most reliable)
pip install advai-cli

# Option 2: npm
npm install -g advai-cli

# Option 3: Homebrew (macOS)
brew tap Advai-X/advai https://github.com/Advai-X/advai-x-cli
brew install advai

# Option 4: one-liner script (macOS / Linux)
curl -fsSL https://raw.githubusercontent.com/Advai-X/advai-x-cli/main/install.sh | bash
```

After installation:

```bash
advai --version
advai --help
advai install demo-skill
advai list
advai info demo-skill
advai uninstall demo-skill
```

---

## Project Structure

```
advai/              # core CLI (Python)
  __init__.py
  cli.py            # entry point (click-based)
  skills.py         # Skill install / uninstall / metadata logic
Formula/advai.rb    # Homebrew formula
bin/advai.js        # npm entry point bridge
install.sh          # curl | bash one-liner script
pyproject.toml      # PyPI build configuration
package.json        # npm package configuration
```

---

## Local Development

```bash
# Run from source
python3 -m advai.cli --help

# Build distribution packages
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload dist/*
```

---

## License

MIT
