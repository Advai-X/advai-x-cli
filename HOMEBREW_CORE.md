# Homebrew Core Submission Notes

This repository is prepared to submit `advai-cli` to `homebrew-core`, but acceptance still depends on Homebrew's external review criteria.

## What Is Already Aligned

- Stable, versioned source release is published on PyPI
- Formula uses `Language::Python::Virtualenv`
- Formula installs from source tarball instead of a wheel
- Python dependency is declared explicitly
- Runtime Python dependency is bundled through `resource` blocks
- Formula test exercises real CLI behavior instead of only `--help`
- Repository includes an OSI-approved `MIT` license
- Package metadata points to the public GitHub repository and issue tracker

## Remaining External Gates

- `homebrew-core` must accept the project name and formula
- The project must meet Homebrew's notability requirements for self-submitted software
- The formula must pass Homebrew CI on supported macOS and Linux targets
- The upstream repository should look active, maintained, and publicly usable

## Local Validation Commands

Run these in a normal local shell before opening a PR. `brew audit` should be run from a `homebrew-core` checkout after copying the formula into `Formula/a/advai-cli.rb`, because Homebrew no longer supports auditing a local path directly:

```bash
brew update
brew tap --force homebrew/core
brew style Formula/advai-cli.rb
brew install --build-from-source ./Formula/advai-cli.rb
brew test advai-cli
```

## Prepare A `homebrew-core` Branch

Clone `homebrew-core`, copy the formula in, and open the PR from your fork:

```bash
git clone https://github.com/Homebrew/homebrew-core.git
cd homebrew-core
git checkout -b advai-cli
cp /path/to/advai-x-cli/Formula/advai-cli.rb Formula/a/advai-cli.rb
brew style Formula/a/advai-cli.rb
brew audit --strict --online advai-cli
git add Formula/a/advai-cli.rb
git commit -m "advai-cli 1.0.6 (new formula)"
```

## PR Notes

- Explain what `advai-cli` does in one sentence
- Link to the upstream GitHub repository
- Link to the stable PyPI release
- Mention that the formula installs a Python application in a virtualenv
- Mention any real-world usage or adopters if available
- Be ready for maintainers to reject the PR if project notability is still too low

## If The PR Is Rejected

The fallback path remains a maintained tap install:

```bash
brew install Advai-X/advai-cli/advai-cli
```
