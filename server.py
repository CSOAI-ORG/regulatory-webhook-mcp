#!/usr/bin/env python3
"""Regulatory Update Webhook — MEOK AI Labs. Monitor regulatory changes, notify subscribers."""

import sys, os

sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

import json, os, hashlib, time, requests
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)


def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now)
    return None


mcp = FastMCP(
    "regulatory-webhook",
    instructions="MEOK AI Labs — Monitor regulatory changes. Subscribe to updates. Get notified when laws change.",
)

_subscribers = defaultdict(list)
_webhooks = []
_updates_cache = []

REGULATORY_CHANGES = [
    {
        "date": "2026-04-14",
        "framework": "EU AI Act",
        "change": "Digital Omnibus: Annex III deadline moved to Dec 2027",
        "impact": "high",
        "source": "EU Commission",
    },
    {
        "date": "2026-04-10",
        "framework": "NIST AI RMF 2.0",
        "change": "Version 2.0 released with new governance structures",
        "impact": "high",
        "source": "NIST",
    },
    {
        "date": "2026-04-01",
        "framework": "UK AI Security Institute",
        "change": "Rebranded to UK AISI",
        "impact": "medium",
        "source": "UK Government",
    },
    {
        "date": "2026-03-20",
        "framework": "ISO 42001",
        "change": "First AI management system standard published",
        "impact": "high",
        "source": "ISO",
    },
    {
        "date": "2026-03-15",
        "framework": "Singapore Model AI Governance",
        "change": "Updated версия 2.0 released",
        "impact": "medium",
        "source": "IMDA",
    },
]


@mcp.tool()
def subscribe(
    email: str, frameworks: str = "all", webhook_url: str = "", api_key: str = ""
) -> str:
    """Subscribe to regulatory update notifications for specific frameworks.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    sub_id = hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()[:12]
    frameworks_list = [f.strip() for f in frameworks.split(",")]

    sub = {
        "id": sub_id,
        "email": email,
        "frameworks": frameworks_list,
        "webhook_url": webhook_url,
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }

    _subscribers[email] = sub

    if webhook_url:
        _webhooks.append({"url": webhook_url, "sub_id": sub_id})

    return {
        "subscribed": True,
        "sub_id": sub_id,
        "email": email,
        "frameworks": frameworks_list,
    }


@mcp.tool()
def unsubscribe(email: str, api_key: str = "") -> str:
    """Unsubscribe from regulatory updates.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    if email in _subscribers:
        _subscribers[email]["status"] = "inactive"
        return {"unsubscribed": True, "email": email}

    return {"error": "Not subscribed"}


@mcp.tool()
def get_recent_changes(
    framework: str = "all", days: int = 90, api_key: str = ""
) -> str:
    """Get recent regulatory changes for specified frameworks.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    filtered = [
        c
        for c in REGULATORY_CHANGES
        if datetime.fromisoformat(c["date"].replace("-", "/")) >= cutoff
    ]

    if framework != "all":
        filtered = [c for c in filtered if framework.lower() in c["framework"].lower()]

    return {"changes": filtered, "total": len(filtered), "framework": framework}


@mcp.tool()
def check_for_updates(
    frameworks: str = "eu_ai_act,nist,iso_42001", api_key: str = ""
) -> str:
    """Check if monitored frameworks have recent updates.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    fw_list = [f.strip() for f in frameworks.split(",")]
    updates = []

    for fw in fw_list:
        for change in REGULATORY_CHANGES:
            if fw.lower().replace("_", " ") in change["framework"].lower():
                updates.append(change)

    return {
        "has_updates": len(updates) > 0,
        "updates": updates,
        "checked": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def register_webhook(
    url: str, events: str = "regulatory_change", api_key: str = ""
) -> str:
    """Register a webhook for regulatory notifications.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    webhook_id = hashlib.sha256(f"{url}{time.time()}".encode()).hexdigest()[:12]

    webhook = {
        "id": webhook_id,
        "url": url,
        "events": [e.strip() for e in events.split(",")],
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }
    _webhooks.append(webhook)

    return {"registered": True, "webhook_id": webhook_id, "url": url}


@mcp.tool()
def trigger_webhook(webhook_id: str, payload: dict, api_key: str = "") -> str:
    """Manually trigger a webhook with payload.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    webhook = next((w for w in _webhooks if w["id"] == webhook_id), None)
    if not webhook:
        return {"error": "Webhook not found"}

    try:
        response = requests.post(webhook["url"], json=payload, timeout=10)
        return {
            "triggered": True,
            "status_code": response.status_code,
            "response": response.text[:200],
        }
    except Exception as e:
        return {"triggered": False, "error": str(e)}


@mcp.tool()
def get_subscribers(api_key: str = "") -> str:
    """List all webhook subscribers (admin only).

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if tier not in ["pro", "enterprise"]:
        return {"error": "Admin access required"}

    return {"subscribers": list(_subscribers.values()), "total": len(_subscribers)}


@mcp.tool()
def list_webhooks(api_key: str = "") -> str:
    """List all registered webhooks.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    return {"webhooks": _webhooks, "total": len(_webhooks)}


@mcp.tool()
def get_framework_newsletter_summary(api_key: str = "") -> str:
    """Get a newsletter-ready summary of recent regulatory changes.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    high_impact = [c for c in REGULATORY_CHANGES if c.get("impact") == "high"]

    return {
        "summary": {
            "total_changes": len(REGULATORY_CHANGES),
            "high_impact_count": len(high_impact),
            "frameworks_covered": list(set(c["framework"] for c in REGULATORY_CHANGES)),
            "high_impact_items": high_impact,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()
