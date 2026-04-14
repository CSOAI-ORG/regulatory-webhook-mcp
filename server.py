#!/usr/bin/env python3
"""Regulatory Update Webhook — MEOK AI Labs. Monitor regulatory changes, notify subscribers."""
import json, os, hashlib, time
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

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
def subscribe(email: str, frameworks: str = "all") -> str:
    """Subscribe to regulatory update notifications."""
    if err := _rl(): return err
    sub = {"email": email, "frameworks": frameworks.split(","), "subscribed": datetime.now(timezone.utc).isoformat(), "id": hashlib.sha256(email.encode()).hexdigest()[:8]}
    _subscribers.append(sub)
    return json.dumps(sub, indent=2)

@mcp.tool()
def get_recent_changes(framework: str = "all", days: int = 90) -> str:
    """Get recent regulatory changes."""
    if err := _rl(): return err
    filtered = _changes if framework == "all" else [c for c in _changes if framework.lower() in c["framework"].lower()]
    return json.dumps({"changes": filtered, "total": len(filtered)}, indent=2)

@mcp.tool()
def check_for_updates(frameworks: str = "eu_ai_act,nist,iso_42001") -> str:
    """Check if any monitored frameworks have recent updates."""
    if err := _rl(): return err
    fw_list = [f.strip() for f in frameworks.split(",")]
    updates = [c for c in _changes if any(f.lower().replace("_"," ") in c["framework"].lower() for f in fw_list)]
    return json.dumps({"has_updates": len(updates) > 0, "updates": updates, "checked": datetime.now(timezone.utc).isoformat()}, indent=2)

@mcp.tool()
def list_subscribers() -> str:
    """List all webhook subscribers."""
    return json.dumps({"subscribers": _subscribers, "total": len(_subscribers)}, indent=2)

if __name__ == "__main__":
    mcp.run()
