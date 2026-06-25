# advai-cli

`advai-cli` is a command-line tool for managing skills and working with external CLIs through a single `advai` entrypoint.

## Features

- Show local `advai` runtime and installation details
- Install, list, inspect, update, and uninstall local skills
- Discover installable external CLIs
- Install third-party CLIs through `advai cli install`
- Execute supported external CLIs through `advai cli <name> ...`
- Chat with AI in a terminal TUI via `advai tui`

## Install

### PyPI

```bash
pip install advai-cli
```

### npm

```bash
npm install -g advai-cli
```

### Homebrew tap

```bash
brew install Advai-X/advai-x-cli/advai-cli
```

## Usage

```bash
advai --help
advai info
advai update
advai tui
```

### TUI chat

Set an OpenAI-compatible API key first:

```bash
export ADVAI_API_KEY=your_api_key
```

Then start the terminal chat UI:

```bash
advai tui
```

Useful options:

```bash
advai tui --model gpt-4o-mini
advai tui --base-url https://api.openai.com/v1
advai tui --system-prompt "You are a concise terminal coding assistant."
```

Environment variables:

```bash
ADVAI_API_KEY
ADVAI_BASE_URL
ADVAI_MODEL
ADVAI_SYSTEM_PROMPT
ADVAI_TIMEOUT
```

TUI commands:

```bash
/help
/clear
/model gpt-4o-mini
/system You are a helpful assistant.
/save ./chat.md
/exit
```

### Skill commands

```bash
advai skill list
advai skill info demo-skill
advai skill install demo-skill
advai skill update demo-skill
advai skill uninstall demo-skill
```

### External CLI commands

```bash
advai cli list
advai cli info demo-cli
advai cli install demo-cli --yes
```
