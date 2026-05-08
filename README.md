<div align="center">

# Regulatory Webhook MCP

**MCP server for regulatory webhook mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-regulatory-webhook-mcp)](https://pypi.org/project/meok-regulatory-webhook-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Regulatory Webhook MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `subscribe` | Subscribe to regulatory update notifications for specific frameworks. |
| `unsubscribe` | Unsubscribe from regulatory updates. |
| `get_recent_changes` | Get recent regulatory changes for specified frameworks. |
| `check_for_updates` | Check if monitored frameworks have recent updates. |
| `register_webhook` | Register a webhook for regulatory notifications. |
| `trigger_webhook` | Manually trigger a webhook with payload. |
| `get_subscribers` | List all webhook subscribers (admin only). |
| `list_webhooks` | List all registered webhooks. |
| `get_framework_newsletter_summary` | Get a newsletter-ready summary of recent regulatory changes. |

## Installation

```bash
pip install meok-regulatory-webhook-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "regulatory-webhook-mcp": {
      "command": "python",
      "args": ["-m", "meok_regulatory_webhook_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 9 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
