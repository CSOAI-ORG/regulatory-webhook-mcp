# Regulatory Webhook

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs — Monitor regulatory changes. Subscribe to updates. Get notified when laws change.

Regulatory Update Webhook — MEOK AI Labs. Monitor regulatory changes, notify subscribers.

## Installation

```bash
pip install regulatory-webhook-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install regulatory-webhook-mcp
```

## Tools

### `subscribe`
Subscribe to regulatory update notifications for specific frameworks.

**Parameters:**
- `email` (str)
- `frameworks` (str)
- `webhook_url` (str)

### `unsubscribe`
Unsubscribe from regulatory updates.

**Parameters:**
- `email` (str)

### `get_recent_changes`
Get recent regulatory changes for specified frameworks.

**Parameters:**
- `framework` (str)
- `days` (int)

### `check_for_updates`
Check if monitored frameworks have recent updates.

**Parameters:**
- `frameworks` (str)

### `register_webhook`
Register a webhook for regulatory notifications.

**Parameters:**
- `url` (str)
- `events` (str)

### `trigger_webhook`
Manually trigger a webhook with payload.

**Parameters:**
- `webhook_id` (str)
- `payload` (str)

### `get_subscribers`
List all webhook subscribers (admin only).

### `list_webhooks`
List all registered webhooks.

### `get_framework_newsletter_summary`
Get a newsletter-ready summary of recent regulatory changes.


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/regulatory-webhook-mcp](https://github.com/CSOAI-ORG/regulatory-webhook-mcp)
- **PyPI**: [pypi.org/project/regulatory-webhook-mcp](https://pypi.org/project/regulatory-webhook-mcp/)

## License

MIT — MEOK AI Labs
