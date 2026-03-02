#!/usr/bin/env python3
"""Clone Resolver - Fuzzy name matching to locate clone agents.

Usage: python3 clone_resolver.py <name_query>

Resolves human-friendly names to agent directory paths.
Searches agents/minds/ and agents/cargo/ directories.
"""
import sys
from pathlib import Path

AGENTS_ROOT = Path(__file__).parent.parent.parent / "agents"

def resolve_clone(query: str) -> dict | None:
    """Resolve a clone name to its agent directory.

    Supports: full name, first name, source code prefix, partial match.
    Returns: {name, path, type} or None
    """
    query_lower = query.strip().lower()
    candidates = []

    for agent_type in ["minds", "cargo"]:
        agent_dir = AGENTS_ROOT / agent_type
        if not agent_dir.exists():
            continue
        for subdir in sorted(agent_dir.iterdir()):
            if not subdir.is_dir() or subdir.name.startswith("_"):
                continue
            name_lower = subdir.name.lower().replace("-", " ")
            if query_lower in name_lower or name_lower in query_lower:
                candidates.append({
                    "name": subdir.name,
                    "path": str(subdir),
                    "type": agent_type,
                    "score": 1.0 if query_lower == name_lower else 0.5
                })

    if not candidates:
        return None
    return sorted(candidates, key=lambda x: x["score"], reverse=True)[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: clone_resolver.py <name_query>")
        sys.exit(1)
    result = resolve_clone(sys.argv[1])
    if result:
        print(f"Found: {result['name']} at {result['path']} (type: {result['type']})")
    else:
        print(f"No clone found matching '{sys.argv[1]}'")
        sys.exit(1)
