# Release Checklist

This document describes the release flow for `advai-cli` across PyPI, npm, and the Homebrew tap.

## Release Model

- Source of truth: Git tag `vX.Y.Z`
- Python distribution: PyPI package `advai-cli`
- npm distribution: npm package `advai-cli`
- Homebrew distribution: tap repository `Advai-X/homebrew-tap`
- Automation entrypoint: [release.yml](../.github/workflows/release.yml)

## Required Secrets

Configure these repository secrets before the first release:

- `PYPI_API_TOKEN`: token for uploading Python distributions to PyPI
- `NPM_TOKEN`: token for publishing `advai-cli` to npm
- `HOMEBREW_TAP_TOKEN`: GitHub token with push access to `Advai-X/homebrew-tap`

## Version Files

Keep the same version in all release metadata:

- `pyproject.toml`
- `package.json`
- `advai/__init__.py`

The release workflow validates that these files match the pushed tag.

## Before Releasing

1. Update the version in:
   - `pyproject.toml`
   - `package.json`
   - `advai/__init__.py`
2. Review local changes:
   ```bash
   git status
   ```
3. Run local verification:
   ```bash
   python -m unittest discover -s tests -p "test_*.py" -v
   npm pack --json --dry-run
   node --check bin/advai.js
   node --check bin/install-python.js
   ```
4. Confirm the Homebrew tap already contains:
   - `Formula/advai-cli.rb`
5. Confirm GitHub secrets are present:
   - `PYPI_API_TOKEN`
   - `NPM_TOKEN`
   - `HOMEBREW_TAP_TOKEN`

## Release Steps

1. Commit the release changes:
   ```bash
   git add .
   git commit -m "Release vX.Y.Z"
   ```
2. Push the branch:
   ```bash
   git push origin main
   ```
3. Create and push the tag:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
4. Wait for the `Release` GitHub Actions workflow to finish.

## What The Workflow Does

When a tag like `v1.0.7` is pushed, the workflow:

1. Validates the tag against:
   - `pyproject.toml`
   - `package.json`
   - `advai/__init__.py`
2. Runs unit tests
3. Verifies the npm package contents with `npm pack --dry-run`
4. Runs CLI smoke tests
5. Builds and publishes the Python package to PyPI
6. Publishes the npm package
7. Fetches the real PyPI sdist URL and SHA256
8. Updates `Advai-X/homebrew-tap/Formula/advai-cli.rb`
9. Commits and pushes the Formula update to the tap repository

## Post-Release Verification

After the workflow succeeds, verify all three distribution channels.

### PyPI

```bash
python -m pip install --upgrade advai-cli==X.Y.Z
advai --version
```

### npm

```bash
npm install -g advai-cli@X.Y.Z
advai --version
```

Expected behavior:

- npm creates a private Python virtual environment during `postinstall`
- the private environment installs the matching `advai-cli` version from PyPI
- `advai --version` prints `X.Y.Z`

### Homebrew

```bash
brew tap Advai-X/tap
brew update
brew upgrade advai-cli || brew install advai-cli
advai --version
```

## Failure Handling

### PyPI Publish Fails

- Check whether the version already exists on PyPI
- Fix the issue in the repository
- Create a new version and tag instead of reusing the failed version number

### npm Publish Fails

- Check whether the version already exists on npm
- Confirm `NPM_TOKEN` is valid
- If PyPI succeeded but npm failed, fix the problem and release a new version

### Homebrew Tap Update Fails

- Confirm `HOMEBREW_TAP_TOKEN` still has push access
- Confirm `Advai-X/homebrew-tap` exists and includes `Formula/advai-cli.rb`
- Re-run the tap update manually if PyPI and npm already succeeded

## Manual Homebrew Recovery

If only the tap update fails, update the Formula manually:

1. Open `Advai-X/homebrew-tap/Formula/advai-cli.rb`
2. Replace:
   - `url`
   - `sha256`
3. Commit and push the tap repository

To get the correct source distribution metadata:

```bash
python - <<'PY'
import json
import urllib.request

version = "X.Y.Z"
with urllib.request.urlopen(f"https://pypi.org/pypi/advai-cli/{version}/json", timeout=30) as response:
    payload = json.load(response)

sdist = next(item for item in payload["urls"] if item["packagetype"] == "sdist")
print(sdist["url"])
print(sdist["digests"]["sha256"])
PY
```
