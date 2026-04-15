#!/usr/bin/env python3
"""Regulatory Update Webhook — MEOK AI Labs. Monitor regulatory changes, notify subscribers."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, os, hashlib, time
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None


_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= 15: return json.dumps({"error": "Limit 15/day"})
    _usage[c].append(now); return None

mcp = FastMCP("regulatory-webhook", instructions="MEOK AI Labs — Monitor regulatory changes. Subscribe to updates. Get notified when laws change.")

_subscribers = []
_changes = [
    {"date": "2026-03-28", "framework": "EU AI Act", "change": "Digital Omnibus: Annex III deadline moved to Dec 2027", "impact": "high"},
    {"date": "2026-01-22", "framework": "South Korea AI Basic Act", "change": "Entered into force", "impact": "high"},
    {"date": "2026-02-01", "framework": "UK AISI", "change": "Rebranded from Safety Institute to Security Institute", "impact": "medium"},
]

@mcp.tool()
def subscribe(email: str, frameworks: str = "all", api_key: str = "") -> str:
    """Subscribe to regulatory update notifications."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    sub = {"email": email, "frameworks": frameworks.split(","), "subscribed": datetime.now(timezone.utc).isoformat(), "id": hashlib.sha256(email.encode()).hexdigest()[:8]}
    _subscribers.append(sub)
    return sub

@mcp.tool()
def get_recent_changes(framework: str = "all", days: int = 90, api_key: str = "") -> str:
    """Get recent regulatory changes."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    filtered = _changes if framework == "all" else [c for c in _changes if framework.lower() in c["framework"].lower()]
    return {"changes": filtered, "total": len(filtered)}

@mcp.tool()
def check_for_updates(frameworks: str = "eu_ai_act,nist,iso_42001", api_key: str = "") -> str:
    """Check if any monitored frameworks have recent updates."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl(): return err
    fw_list = [f.strip() for f in frameworks.split(",")]
    updates = [c for c in _changes if any(f.lower().replace("_"," ") in c["framework"].lower() for f in fw_list)]
    return {"has_updates": len(updates) > 0, "updates": updates, "checked": datetime.now(timezone.utc).isoformat()}

@mcp.tool()
def list_subscribers(api_key: str = "") -> str:
    """List all webhook subscribers."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    return {"subscribers": _subscribers, "total": len(_subscribers)}
    return {"subscribers": _subscribers, "total": len(_subscribers)}

if __name__ == "__main__":
    mcp.run()
