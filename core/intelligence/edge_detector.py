#!/usr/bin/env python3
"""
EDGE DETECTOR - Intelligence Layer v1.0
=========================================
Detects conceptual edges between DNA elements for mind mapping.

Analyzes DNA layers to find relationships between philosophies, mental models,
heuristics, frameworks, methodologies, case studies, anti-patterns, and triggers.

Edge types:
- SUPPORTS:      Element A reinforces Element B
- CONTRADICTS:   Element A conflicts with Element B
- REFINES:       Element A is a more specific version of Element B
- IMPLEMENTS:    Element A is a concrete implementation of Element B
- DERIVES_FROM:  Element A was derived from Element B

Usage:
  python3 edge_detector.py --person <name>           # Detect edges for a person
  python3 edge_detector.py --dna <path>              # Detect edges from DNA path
  python3 edge_detector.py --person <name> --output <path>  # Save to file

Versao: 1.0.0
Data: 2026-03-01
"""

import json
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from clone_resolver import resolve_clone

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
KNOWLEDGE_DNA = BASE_DIR.parent / "knowledge" / "dna"
LOG_PATH = BASE_DIR.parent / "logs" / "edge_detection.jsonl"

# ---------------------------------------------------------------------------
# LAYER HIERARCHY (higher layers are more abstract)
# ---------------------------------------------------------------------------
LAYER_HIERARCHY = {
    "philosophies":        {"level": 1, "id_prefix": "FIL", "nature": "abstract"},
    "mental_models":       {"level": 2, "id_prefix": "MM",  "nature": "abstract"},
    "heuristics":          {"level": 3, "id_prefix": "HEUR", "nature": "concrete"},
    "frameworks":          {"level": 4, "id_prefix": "FW",  "nature": "concrete"},
    "methodologies":       {"level": 5, "id_prefix": "MET", "nature": "concrete"},
    "case_studies":        {"level": 6, "id_prefix": "CS",  "nature": "concrete"},
    "anti_patterns":       {"level": 7, "id_prefix": "AP",  "nature": "concrete"},
    "contextual_triggers": {"level": 8, "id_prefix": "CT",  "nature": "contextual"},
}

# Relationship rules: what edges are likely between layer pairs
RELATIONSHIP_RULES = {
    # (from_nature, to_nature) -> likely relationship
    ("abstract", "concrete"):  "IMPLEMENTS",
    ("concrete", "abstract"):  "DERIVES_FROM",
    ("abstract", "abstract"):  "SUPPORTS",
    ("concrete", "concrete"):  "REFINES",
}

# Keywords that signal contradiction
CONTRADICTION_SIGNALS = [
    "never", "always", "opposite", "instead", "wrong", "mistake",
    "avoid", "don't", "not", "contra", "exception", "unless",
]

# Keywords that signal support/reinforcement
SUPPORT_SIGNALS = [
    "because", "therefore", "aligns", "consistent", "reinforces",
    "builds on", "extends", "similar", "same", "also", "confirms",
]


# ---------------------------------------------------------------------------
# CORE: LOAD DNA ELEMENTS
# ---------------------------------------------------------------------------
def _load_dna_from_path(dna_path: Path) -> dict[str, list[dict]]:
    """Load all DNA layer files from a directory.

    Returns: {layer_name: [items]}
    """
    layers = {}
    if not dna_path.exists() or not dna_path.is_dir():
        return layers

    for yaml_file in sorted(dna_path.glob("*.yaml")):
        raw = None
        with open(yaml_file, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        if not raw or not isinstance(raw, dict):
            continue

        layer_name = yaml_file.stem.lower().replace("-", "_")
        # Normalize: items may be under 'items', layer_name, or top-level list key
        items = raw.get("items", [])
        if not items:
            for key in raw:
                if isinstance(raw[key], list):
                    items = raw[key]
                    break
        if not items and isinstance(raw, dict):
            # Single-layer file: treat all dict entries as items
            items = [raw]

        # Normalize items to have at minimum {id, text}
        normalized = []
        for item in items:
            if not isinstance(item, dict):
                continue
            normalized.append({
                "id": item.get("id", f"{layer_name}-{len(normalized)+1:03d}"),
                "text": _extract_text(item),
                "domain": item.get("domain", item.get("domains", "")),
                "source": item.get("source", item.get("sources", [])),
                "layer": layer_name,
                "raw": item,
            })

        if normalized:
            layers[layer_name] = normalized

    return layers


def _load_dna_for_person(person_query: str) -> tuple[dict[str, list[dict]], str]:
    """Resolve person name and load their DNA.

    Returns: (layers_dict, person_name)
    """
    # Try knowledge/dna/persons/ first
    persons_dir = KNOWLEDGE_DNA / "persons"
    if persons_dir.exists():
        for subdir in sorted(persons_dir.iterdir()):
            if not subdir.is_dir():
                continue
            if person_query.lower().replace(" ", "-") in subdir.name.lower():
                return _load_dna_from_path(subdir), subdir.name

    # Try via clone_resolver -> DNA-CONFIG.yaml -> dna_sources paths
    resolved = resolve_clone(person_query)
    if resolved:
        agent_path = Path(resolved["path"])
        dna_config_path = agent_path / "DNA-CONFIG.yaml"
        if dna_config_path.exists():
            with open(dna_config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if config:
                sources = config.get("dna_sources", {})
                all_layers = {}
                for source_type in ["primario", "agregado"]:
                    for source in sources.get(source_type, []):
                        dna_path = Path(BASE_DIR.parent) / source.get("path", "").lstrip("/")
                        if dna_path.exists() and dna_path.is_dir():
                            layers = _load_dna_from_path(dna_path)
                            for k, v in layers.items():
                                all_layers.setdefault(k, []).extend(v)
                return all_layers, resolved["name"]

    return {}, person_query


def _extract_text(item: dict) -> str:
    """Extract the primary text content from a DNA item."""
    for key in ["statement", "rule", "description", "name", "text",
                "principle", "belief", "trigger", "pattern", "summary"]:
        val = item.get(key, "")
        if val and isinstance(val, str):
            return val
    # Fallback: concatenate all string values
    parts = [str(v) for v in item.values() if isinstance(v, str) and len(str(v)) > 5]
    return " | ".join(parts[:3]) if parts else str(item.get("id", ""))


# ---------------------------------------------------------------------------
# CORE: EDGE DETECTION
# ---------------------------------------------------------------------------
def _tokenize(text: str) -> set[str]:
    """Simple word tokenization for comparison."""
    return set(re.findall(r'\b[a-z]{3,}\b', text.lower()))


def _word_overlap(tokens_a: set[str], tokens_b: set[str]) -> float:
    """Calculate Jaccard similarity between token sets."""
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def _domain_overlap(domain_a, domain_b) -> bool:
    """Check if two items share a domain."""
    def normalize_domain(d):
        if isinstance(d, list):
            return set(str(x).lower() for x in d)
        return {str(d).lower()} if d else set()

    da = normalize_domain(domain_a)
    db = normalize_domain(domain_b)
    return bool(da & db)


def _classify_relationship(item_a: dict, item_b: dict, similarity: float) -> tuple[str, float]:
    """Classify the relationship between two DNA elements.

    Returns: (edge_type, confidence)
    """
    text_a = item_a["text"].lower()
    text_b = item_b["text"].lower()
    layer_a = item_a["layer"]
    layer_b = item_b["layer"]

    # Check for contradiction signals
    contradiction_score = 0
    for signal in CONTRADICTION_SIGNALS:
        if signal in text_a or signal in text_b:
            contradiction_score += 1

    # Anti-patterns layer: high contradiction probability with other layers
    if layer_a.startswith("anti_pattern") or layer_b.startswith("anti_pattern"):
        if similarity > 0.15:
            return "CONTRADICTS", min(0.5 + similarity, 0.95)

    # Strong contradiction signals + shared domain
    if contradiction_score >= 2 and _domain_overlap(item_a["domain"], item_b["domain"]):
        return "CONTRADICTS", min(0.4 + similarity * 0.5, 0.85)

    # Same layer -> REFINES (one refines the other)
    if layer_a == layer_b and similarity > 0.2:
        return "REFINES", min(0.3 + similarity, 0.90)

    # Abstract -> Concrete: IMPLEMENTS
    nature_a = LAYER_HIERARCHY.get(layer_a, {}).get("nature", "concrete")
    nature_b = LAYER_HIERARCHY.get(layer_b, {}).get("nature", "concrete")
    level_a = LAYER_HIERARCHY.get(layer_a, {}).get("level", 5)
    level_b = LAYER_HIERARCHY.get(layer_b, {}).get("level", 5)

    if nature_a == "abstract" and nature_b == "concrete" and level_a < level_b:
        return "IMPLEMENTS", min(0.3 + similarity, 0.90)

    if nature_a == "concrete" and nature_b == "abstract" and level_a > level_b:
        return "DERIVES_FROM", min(0.3 + similarity, 0.90)

    # Default: SUPPORTS
    support_score = sum(1 for s in SUPPORT_SIGNALS if s in text_a or s in text_b)
    confidence = min(0.2 + similarity + (support_score * 0.05), 0.90)
    return "SUPPORTS", confidence


def detect_edges(
    dna_path: str | None = None,
    person: str | None = None,
    min_similarity: float = 0.15,
    min_confidence: float = 0.3,
) -> dict:
    """Detect conceptual edges between DNA elements.

    Returns:
        {
            "person": str,
            "generated_at": str,
            "total_elements": int,
            "total_edges": int,
            "edges": [
                {
                    "from_id": str,
                    "from_layer": str,
                    "from_text": str,
                    "to_id": str,
                    "to_layer": str,
                    "to_text": str,
                    "relationship": str,
                    "confidence": float,
                    "shared_domain": bool,
                }
            ],
            "summary": {
                "by_type": {type: count},
                "by_layer_pair": {pair: count},
                "strongest_edges": [top 5],
            },
        }
    """
    # Load DNA
    if person:
        layers, person_name = _load_dna_for_person(person)
    elif dna_path:
        layers = _load_dna_from_path(Path(dna_path))
        person_name = Path(dna_path).name
    else:
        return {"error": "Provide --person or --dna", "edges": [], "total_edges": 0}

    if not layers:
        return {
            "person": person_name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_elements": 0,
            "total_edges": 0,
            "edges": [],
            "summary": {},
            "error": f"No DNA layers found for '{person_name}'.",
        }

    # Flatten all items
    all_items = []
    for layer_name, items in layers.items():
        all_items.extend(items)

    # Pre-tokenize
    token_cache = {}
    for item in all_items:
        token_cache[item["id"]] = _tokenize(item["text"])

    # Compare all pairs (O(n^2) but DNA sets are small, typically < 200 items)
    edges = []
    seen_pairs = set()

    for i, item_a in enumerate(all_items):
        for j, item_b in enumerate(all_items):
            if i >= j:
                continue

            pair_key = (item_a["id"], item_b["id"])
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            # Skip same-item comparison
            if item_a["id"] == item_b["id"]:
                continue

            # Calculate similarity
            tokens_a = token_cache[item_a["id"]]
            tokens_b = token_cache[item_b["id"]]
            similarity = _word_overlap(tokens_a, tokens_b)

            if similarity < min_similarity:
                continue

            # Classify relationship
            edge_type, confidence = _classify_relationship(item_a, item_b, similarity)

            if confidence < min_confidence:
                continue

            shared_domain = _domain_overlap(item_a["domain"], item_b["domain"])

            # Boost confidence for shared domain
            if shared_domain:
                confidence = min(confidence + 0.1, 0.95)

            edges.append({
                "from_id": item_a["id"],
                "from_layer": item_a["layer"],
                "from_text": item_a["text"][:120],
                "to_id": item_b["id"],
                "to_layer": item_b["layer"],
                "to_text": item_b["text"][:120],
                "relationship": edge_type,
                "confidence": round(confidence, 3),
                "shared_domain": shared_domain,
            })

    # Sort by confidence descending
    edges.sort(key=lambda e: -e["confidence"])

    # Build summary
    by_type = {}
    by_layer_pair = {}
    for edge in edges:
        by_type[edge["relationship"]] = by_type.get(edge["relationship"], 0) + 1
        pair = f"{edge['from_layer']} <-> {edge['to_layer']}"
        by_layer_pair[pair] = by_layer_pair.get(pair, 0) + 1

    result = {
        "person": person_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_elements": len(all_items),
        "layers_loaded": list(layers.keys()),
        "total_edges": len(edges),
        "edges": edges,
        "summary": {
            "by_type": dict(sorted(by_type.items(), key=lambda x: -x[1])),
            "by_layer_pair": dict(sorted(by_layer_pair.items(), key=lambda x: -x[1])[:10]),
            "strongest_edges": [
                {
                    "from": e["from_id"],
                    "to": e["to_id"],
                    "type": e["relationship"],
                    "confidence": e["confidence"],
                }
                for e in edges[:5]
            ],
        },
    }

    _log_detection(result)
    return result


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
def _log_detection(result: dict):
    """Log edge detection to JSONL."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trigger_type": "edge_detection",
        "person": result["person"],
        "total_elements": result["total_elements"],
        "total_edges": result["total_edges"],
        "by_type": result.get("summary", {}).get("by_type", {}),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]

    if not args or "--help" in args:
        print("Usage:")
        print("  python3 edge_detector.py --person 'Alex Hormozi'         # By person name")
        print("  python3 edge_detector.py --dna <path>                    # By DNA directory")
        print("  python3 edge_detector.py --person <name> --output <path> # Save to file")
        sys.exit(1)

    person = None
    dna_path = None
    output_path = None

    for i, arg in enumerate(args):
        if arg == "--person" and i + 1 < len(args):
            person = args[i + 1]
        elif arg == "--dna" and i + 1 < len(args):
            dna_path = args[i + 1]
        elif arg == "--output" and i + 1 < len(args):
            output_path = args[i + 1]

    print(f"\n=== EDGE DETECTOR v1.0 ===\n")

    result = detect_edges(dna_path=dna_path, person=person)

    if result.get("error"):
        print(f"  ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Person: {result['person']}")
    print(f"  Layers: {', '.join(result.get('layers_loaded', []))}")
    print(f"  Elements: {result['total_elements']}")
    print(f"  Edges detected: {result['total_edges']}")
    print()

    # Summary by type
    summary = result.get("summary", {})
    by_type = summary.get("by_type", {})
    if by_type:
        print("  Edge Types:")
        for edge_type, count in by_type.items():
            print(f"    {edge_type:15s}: {count}")
        print()

    # Strongest edges
    strongest = summary.get("strongest_edges", [])
    if strongest:
        print("  Strongest Edges:")
        for edge in strongest:
            print(f"    {edge['from']:15s} --[{edge['type']:12s}]--> {edge['to']:15s}  ({edge['confidence']:.2f})")
        print()

    # Save if output path
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"  Saved to: {output_path}")


if __name__ == "__main__":
    main()
