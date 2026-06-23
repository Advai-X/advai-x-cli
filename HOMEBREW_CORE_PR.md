# Homebrew Core PR Draft

The only path to support:

```bash
brew install advai-cli
```

is to get `advai-cli` accepted into `homebrew-core`.

This file contains a ready-to-use PR draft for that submission.

## PR Title

```text
advai-cli 1.0.4 (new formula)
```

## Commit Message In `homebrew-core`

```text
advai-cli 1.0.4 (new formula)
```

## Suggested PR Body

```markdown
## What does this PR do?

Adds a new `homebrew-core` formula for `advai-cli`.

`advai-cli` is a command-line tool for managing AdvAI skills and working with external CLIs through a single `advai` entrypoint.

## Upstream

- Repository: https://github.com/Advai-X/advai-x-cli
- PyPI: https://pypi.org/project/advai-cli/

## Installation model

This formula packages a Python application using `Language::Python::Virtualenv` and installs from the upstream source tarball published on PyPI.

## Validation

I ran:

```bash
brew style Formula/a/advai-cli.rb
brew audit --new --strict --online Formula/a/advai-cli.rb
brew install --build-from-source Formula/a/advai-cli.rb
brew test advai-cli
```
```

## One-Sentence Project Description

Use this sentence consistently in the PR and any maintainer replies:

```text
advai-cli is a Python-based command-line tool for managing AdvAI skills and invoking supported external CLIs from a single advai entrypoint.
```

## Likely Maintainer Questions

### Why should this be in `homebrew-core`?

Suggested answer:

```markdown
`advai-cli` is an end-user command-line application, not a Python library. It has a stable tagged release, a PyPI source tarball, an open-source MIT license, and a formula that uses Homebrew's standard Python virtualenv packaging flow.
```

### Does it self-update?

Suggested answer:

```markdown
No. The CLI does not perform in-place self-updates. Its `advai update` command only prints the recommended package-manager command for the current installation method.
```

### Why package this instead of asking users to use `pip`?

Suggested answer:

```markdown
This is an end-user CLI application. Homebrew provides a more standard installation path for macOS users who expect `brew install <tool>` for command-line utilities.
```

### What does the test cover?

Suggested answer:

```markdown
The formula test verifies the installed binary reports its version and can perform a real local skill workflow: install a skill, list it, and read its metadata.
```

## Local Submission Steps

```bash
git clone https://github.com/<your-fork>/homebrew-core.git
cd homebrew-core
git checkout -b advai-cli
mkdir -p Formula/a
cp /Users/xuyi/Documents/workspace/advai-x-cli/Formula/advai-cli.rb Formula/a/advai-cli.rb
export HOMEBREW_NO_INSTALL_FROM_API=1
brew style Formula/a/advai-cli.rb
brew audit --new --strict --online Formula/a/advai-cli.rb
brew install --build-from-source Formula/a/advai-cli.rb
brew test advai-cli
git add Formula/a/advai-cli.rb
git commit -m "advai-cli 1.0.4 (new formula)"
git push origin advai-cli
```

## Important Reality Check

Even with a clean formula, Homebrew maintainers may still reject the PR if the project does not meet `homebrew-core` notability expectations for self-submitted software.

If that happens, the fallback distribution path remains:

```bash
brew install Advai-X/advai-x-cli/advai-cli
```
