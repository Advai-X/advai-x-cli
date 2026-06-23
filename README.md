# advai-cli

A cross-platform CLI tool for skill management and CLI self-management.

Install:
```bash
pip install advai-cli
```

Commands:
```bash
advai --help
advai skill list
advai skill install demo-skill
advai cli list
advai cli info
advai cli update --yes
```

Structured command groups:
```bash
advai skill list
advai skill info demo-skill
advai skill install demo-skill
advai skill update demo-skill
advai skill uninstall demo-skill
```

CLI management:
```bash
advai cli list
advai cli info
advai cli install --manager pip --yes
advai cli update --manager pip --yes
advai cli uninstall --manager pip --yes
```
