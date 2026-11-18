# Maestro Model Context Protocol (MCP) Integration

This guide details how AI agents (such as Antigravity, Claude Code, Cursor, and Codex) interact with live mobile emulators using the **Maestro MCP Server**.

---

## 1. Overview

The Maestro MCP server exposes Maestro's device inspection and automation engine directly over STDIO as standard MCP tools. This enables AI models to:
- Inspect screens and extract view hierarchies in real time.
- Take screenshots during test authoring or failure diagnosis.
- Drive live Android emulators or iOS simulators conversationally.
- Self-heal failing tests without leaving the coding chat.

---

## 2. MCP Server Configuration

Configured in `~/.gemini/config/mcp_config.json` and `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "maestro": {
      "command": "/Users/reza/.maestro/bin/maestro",
      "args": ["mcp"],
      "env": {
        "JAVA_HOME": "/opt/homebrew/opt/openjdk@21",
        "ANDROID_HOME": "/Library/Android/sdk",
        "PATH": "/opt/homebrew/opt/openjdk@21/bin:/Library/Android/sdk/platform-tools:/Library/Android/sdk/emulator:/Users/reza/.maestro/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
      }
    }
  }
}
```

---

## 3. Core Tools Reference

### 3.1 `list_devices`
Lists all locally attached Android emulators, physical devices, or iOS simulators.
```json
{}
```
*Returns*: A list of connected devices with their `device_id` (e.g. `emulator-5554`).

### 3.2 `inspect_screen`
Extracts the full accessibility hierarchy of the current screen. Always run before authoring new locators:
```json
{
  "device_id": "emulator-5554"
}
```

### 3.3 `take_screenshot`
Captures a screenshot of the live device:
```json
{
  "device_id": "emulator-5554"
}
```

### 3.4 `run`
Executes Maestro commands or flow files on the target device:
```json
{
  "device_id": "emulator-5554",
  "files": ["flows/kasir/catalog_qty_flow.yaml"],
  "env": {
    "APP_ID": "com.cloudiex.possaku"
  }
}
```
Or executes inline exploratory commands:
```json
{
  "device_id": "emulator-5554",
  "yaml": "- tapOn: 'Kasir\\n'\n- assertVisible: 'Keranjang.*'"
}
```

### 3.5 `cheat_sheet`
Retrieves up-to-date syntax, supported commands, and options for Maestro flows.

