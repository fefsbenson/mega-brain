#!/usr/bin/env python3
"""
BLIND TEST GENERATOR - Intelligence Layer v1.0
================================================
Generates fidelity test scenarios for clone validation.

Creates structured test prompts that probe each DNA layer to verify
whether a clone responds authentically based on its SOUL, MEMORY, and DNA.

Test types:
- LAYER_PROBE: Direct question targeting a specific DNA layer
- CROSS_LAYER: Scenario requiring multiple layers to answer
- CONTRADICTION: Question where sources disagree (tests conflict handling)
- EDGE_CASE: Scenario outside documented expertise (tests epistemic honesty)

Usage:
  python3 blind_test_generator.py <clone_id>           # Generate tests for clone
  python3 blind_test_generator.py <clone_id> --output <path>  # Save to file
  python3 blind_test_generator.py --all                 # Generate for all clones

Versao: 1.0.0
Data: 2026-03-01
"""

import json
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
AGENTS_ROOT = BASE_DIR.parent / "agents"
KNOWLEDGE_DNA = BASE_DIR.parent / "knowledge" / "dna"
LOG_PATH = BASE_DIR.parent / "logs" / "blind_tests.jsonl"

# ---------------------------------------------------------------------------
# DNA LAYERS (8-layer schema)
# ---------------------------------------------------------------------------
DNA_LAYERS = {
    "L1_philosophies": {
        "name": "Philosophies",
        "id_prefix": "FIL",
        "probe_templates": [
            "What is your core belief about {domain}?",
            "If you had to summarize your philosophy on {topic} in one sentence, what would it be?",
            "What principle guides every decision you make about {domain}?",
        ],
    },
    "L2_mental_models": {
        "name": "Mental Models",
        "id_prefix": "MM",
        "probe_templates": [
            "How do you think about {topic}? What mental model do you use?",
            "What analogy best describes your approach to {domain}?",
            "When faced with {scenario}, what framework guides your thinking?",
        ],
    },
    "L3_heuristics": {
        "name": "Heuristics",
        "id_prefix": "HEUR",
        "probe_templates": [
            "What's your rule of thumb for {topic}?",
            "Give me a specific number or threshold for {metric}.",
            "What's the quick test you use to evaluate {domain}?",
        ],
    },
    "L4_frameworks": {
        "name": "Frameworks",
        "id_prefix": "FW",
        "probe_templates": [
            "Walk me through your framework for {topic}.",
            "What are the key components of your {domain} system?",
            "How do you structure your approach to {scenario}?",
        ],
    },
    "L5_methodologies": {
        "name": "Methodologies",
        "id_prefix": "MET",
        "probe_templates": [
            "Give me the step-by-step process for {topic}.",
            "If I had to implement {domain} tomorrow, what are the exact steps?",
            "What's the sequence you follow for {scenario}?",
        ],
    },
    "L6_case_studies": {
        "name": "Case Studies",
        "id_prefix": "CS",
        "probe_templates": [
            "Give me a real example of {topic} in action.",
            "Tell me about a time when {scenario} happened and what you did.",
            "What's a concrete case that illustrates your approach to {domain}?",
        ],
    },
    "L7_anti_patterns": {
        "name": "Anti-Patterns",
        "id_prefix": "AP",
        "probe_templates": [
            "What's the biggest mistake people make with {topic}?",
            "What should I absolutely NOT do when it comes to {domain}?",
            "What's the most common failure mode in {scenario}?",
        ],
    },
    "L8_contextual_triggers": {
        "name": "Contextual Triggers",
        "id_prefix": "CT",
        "probe_templates": [
            "When exactly should I apply {framework} vs {alternative}?",
            "What signals tell you it's time to change approach in {domain}?",
            "Under what conditions does your {topic} advice NOT apply?",
        ],
    },
}

# ---------------------------------------------------------------------------
# TEST TYPES
# ---------------------------------------------------------------------------
TEST_TYPES = {
    "LAYER_PROBE": {
        "description": "Direct question targeting a specific DNA layer",
        "weight": 1.0,
    },
    "CROSS_LAYER": {
        "description": "Scenario requiring multiple layers to answer well",
        "weight": 1.5,
    },
    "CONTRADICTION": {
        "description": "Question where sources may disagree",
        "weight": 2.0,
    },
    "EDGE_CASE": {
        "description": "Scenario outside documented expertise",
        "weight": 1.5,
    },
}

CROSS_LAYER_TEMPLATES = [
    "A client says '{objection}'. Using your {framework}, walk me through "
    "exactly how you'd handle this — include the philosophy behind it and "
    "any specific numbers I should know.",
    "I'm building a {domain} system from scratch. Give me the methodology, "
    "the key heuristics, and the mental model I should use to evaluate progress.",
    "Compare your approach to {topic_a} vs {topic_b}. Where do they align "
    "and where do they diverge?",
]

EDGE_CASE_TEMPLATES = [
    "What's your take on {unrelated_domain}?",
    "How would you handle {scenario} in a market you've never worked in?",
    "If all your usual approaches failed, what would you do about {topic}?",
]


# ---------------------------------------------------------------------------
# CORE: LOAD CLONE DATA
# ---------------------------------------------------------------------------
def _load_clone_data(clone_id: str) -> dict | None:
    """Load all relevant data for a clone (DNA-CONFIG, SOUL, MEMORY)."""
    resolved = resolve_clone(clone_id)
    if not resolved:
        return None

    agent_path = Path(resolved["path"])
    data = {
        "name": resolved["name"],
        "path": resolved["path"],
        "type": resolved["type"],
        "dna_config": None,
        "soul": None,
        "memory": None,
        "dna_layers": {},
    }

    # Load DNA-CONFIG.yaml
    dna_config_path = agent_path / "DNA-CONFIG.yaml"
    if dna_config_path.exists():
        with open(dna_config_path, "r", encoding="utf-8") as f:
            data["dna_config"] = yaml.safe_load(f)

    # Load SOUL.md (extract key sections)
    soul_path = agent_path / "SOUL.md"
    if soul_path.exists():
        data["soul"] = soul_path.read_text(encoding="utf-8")

    # Load MEMORY.md
    memory_path = agent_path / "MEMORY.md"
    if memory_path.exists():
        data["memory"] = memory_path.read_text(encoding="utf-8")

    # Load DNA layers from knowledge base
    if data["dna_config"]:
        sources = data["dna_config"].get("dna_sources", {})
        for source_type in ["primario", "agregado"]:
            for source in sources.get(source_type, []):
                dna_path = Path(BASE_DIR.parent) / source.get("path", "").lstrip("/")
                if dna_path.exists() and dna_path.is_dir():
                    for yaml_file in dna_path.glob("*.yaml"):
                        layer_name = yaml_file.stem.lower()
                        with open(yaml_file, "r", encoding="utf-8") as f:
                            layer_data = yaml.safe_load(f)
                            if layer_data:
                                data["dna_layers"][layer_name] = layer_data

    return data


def _extract_domains(clone_data: dict) -> list[str]:
    """Extract domain topics from clone's DNA config."""
    domains = []
    if clone_data.get("dna_config"):
        sources = clone_data["dna_config"].get("dna_sources", {})
        for source_type in ["primario", "agregado"]:
            for source in sources.get(source_type, []):
                for d in source.get("dominios_usados", []):
                    if d not in domains:
                        domains.append(d)
    return domains if domains else ["sales", "business", "strategy"]


def _extract_frameworks(clone_data: dict) -> list[str]:
    """Extract named frameworks from DNA layers."""
    frameworks = []
    for layer_name, layer_data in clone_data.get("dna_layers", {}).items():
        if isinstance(layer_data, dict):
            items = layer_data.get("items", layer_data.get("frameworks", []))
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        name = item.get("name", item.get("id", ""))
                        if name:
                            frameworks.append(name)
    return frameworks[:10]


def _extract_heuristics_with_numbers(clone_data: dict) -> list[dict]:
    """Extract heuristics that contain specific numbers/thresholds."""
    heuristics = []
    for layer_name, layer_data in clone_data.get("dna_layers", {}).items():
        if "heuristic" not in layer_name and "heur" not in layer_name:
            continue
        if isinstance(layer_data, dict):
            items = layer_data.get("items", layer_data.get("heuristics", []))
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        rule = item.get("rule", item.get("statement", ""))
                        if any(c.isdigit() for c in str(rule)):
                            heuristics.append({
                                "id": item.get("id", "unknown"),
                                "rule": rule,
                                "threshold": item.get("threshold", ""),
                            })
    return heuristics[:10]


# ---------------------------------------------------------------------------
# CORE: GENERATE TESTS
# ---------------------------------------------------------------------------
def generate_blind_test(clone_id: str, output_path: str | None = None) -> dict:
    """Generate blind test scenarios for a clone.

    Returns:
        {
            "clone_id": str,
            "clone_name": str,
            "generated_at": str,
            "total_tests": int,
            "tests": [
                {
                    "test_id": str,
                    "type": str,
                    "layer": str,
                    "prompt": str,
                    "expected_signals": [str],
                    "red_flags": [str],
                    "weight": float,
                }
            ],
            "scoring_guide": dict,
        }
    """
    clone_data = _load_clone_data(clone_id)
    if not clone_data:
        return {
            "clone_id": clone_id,
            "clone_name": "NOT_FOUND",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_tests": 0,
            "tests": [],
            "scoring_guide": {},
            "error": f"Clone '{clone_id}' not found. Use clone_resolver.py to check.",
        }

    domains = _extract_domains(clone_data)
    frameworks = _extract_frameworks(clone_data)
    heuristics = _extract_heuristics_with_numbers(clone_data)
    tests = []
    test_counter = 0

    # --- LAYER PROBE tests (one per layer that has data) ---
    for layer_id, layer_meta in DNA_LAYERS.items():
        domain = domains[test_counter % len(domains)] if domains else "business"
        template = layer_meta["probe_templates"][test_counter % len(layer_meta["probe_templates"])]
        prompt = template.format(
            domain=domain,
            topic=domain,
            metric=f"{domain} performance",
            scenario=f"a {domain} challenge",
            framework=frameworks[0] if frameworks else "your main framework",
            alternative="an alternative approach",
        )

        expected_signals = [
            f"References {layer_meta['id_prefix']}-prefixed concepts",
            f"Uses vocabulary consistent with {layer_meta['name']} layer",
        ]

        # Add specific expected signals for heuristics layer
        if layer_id == "L3_heuristics" and heuristics:
            h = heuristics[0]
            expected_signals.append(f"Mentions specific threshold: {h.get('threshold', h.get('rule', ''))}")

        red_flags = [
            "Generic advice without domain-specific detail",
            "Claims expertise not documented in DNA",
            f"Missing {layer_meta['name']} depth — too abstract or too vague",
        ]

        test_counter += 1
        tests.append({
            "test_id": f"BT-{clone_id[:4].upper()}-{test_counter:03d}",
            "type": "LAYER_PROBE",
            "layer": layer_id,
            "prompt": prompt,
            "expected_signals": expected_signals,
            "red_flags": red_flags,
            "weight": TEST_TYPES["LAYER_PROBE"]["weight"],
        })

    # --- CROSS LAYER tests ---
    for i, template in enumerate(CROSS_LAYER_TEMPLATES):
        fw = frameworks[i % len(frameworks)] if frameworks else "your primary framework"
        d = domains[i % len(domains)] if domains else "business"
        prompt = template.format(
            objection="I need to think about it",
            framework=fw,
            domain=d,
            topic_a=domains[0] if domains else "sales",
            topic_b=domains[1] if len(domains) > 1 else "marketing",
        )
        test_counter += 1
        tests.append({
            "test_id": f"BT-{clone_id[:4].upper()}-{test_counter:03d}",
            "type": "CROSS_LAYER",
            "layer": "multi",
            "prompt": prompt,
            "expected_signals": [
                "Integrates multiple DNA layers in response",
                "Cites specific frameworks AND heuristics together",
                "Demonstrates philosophical consistency across layers",
            ],
            "red_flags": [
                "Only addresses one layer",
                "Contradicts own philosophy without acknowledging tension",
                "Gives generic multi-step answer without DNA depth",
            ],
            "weight": TEST_TYPES["CROSS_LAYER"]["weight"],
        })

    # --- CONTRADICTION tests (if clone has multiple sources) ---
    if clone_data.get("dna_config"):
        sources = clone_data["dna_config"].get("dna_sources", {})
        primario = sources.get("primario", [])
        if len(primario) >= 2:
            test_counter += 1
            p1 = primario[0].get("pessoa", "Source A")
            p2 = primario[1].get("pessoa", "Source B")
            tests.append({
                "test_id": f"BT-{clone_id[:4].upper()}-{test_counter:03d}",
                "type": "CONTRADICTION",
                "layer": "conflict_resolution",
                "prompt": (
                    f"I've heard conflicting advice: one expert says to focus on "
                    f"volume, another says focus on margin. What's your position?"
                ),
                "expected_signals": [
                    "Acknowledges the tension explicitly",
                    f"References specific sources ({p1}, {p2}) if applicable",
                    "Provides contextual resolution (when each applies)",
                    "Declares confidence level",
                ],
                "red_flags": [
                    "Picks one side without acknowledging the other",
                    "Presents as settled when sources genuinely disagree",
                    "No mention of context-dependent resolution",
                ],
                "weight": TEST_TYPES["CONTRADICTION"]["weight"],
            })

    # --- EDGE CASE tests ---
    unrelated_domains = ["quantum physics", "medieval history", "marine biology"]
    for i, template in enumerate(EDGE_CASE_TEMPLATES[:2]):
        test_counter += 1
        prompt = template.format(
            unrelated_domain=unrelated_domains[i % len(unrelated_domains)],
            scenario="a completely unfamiliar market",
            topic=domains[0] if domains else "business",
        )
        tests.append({
            "test_id": f"BT-{clone_id[:4].upper()}-{test_counter:03d}",
            "type": "EDGE_CASE",
            "layer": "epistemic_honesty",
            "prompt": prompt,
            "expected_signals": [
                "Admits limitation or lack of expertise",
                "Says 'I don't have sources for this' or equivalent",
                "Declares low confidence",
                "Suggests where to look instead",
            ],
            "red_flags": [
                "Confidently answers outside documented expertise",
                "No epistemic qualification",
                "Invents data or frameworks not in DNA",
            ],
            "weight": TEST_TYPES["EDGE_CASE"]["weight"],
        })

    # Build result
    result = {
        "clone_id": clone_id,
        "clone_name": clone_data["name"],
        "clone_type": clone_data["type"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(tests),
        "domains_tested": domains,
        "frameworks_referenced": frameworks,
        "tests": tests,
        "scoring_guide": {
            "per_test": "Each test scored 0-10 based on expected_signals hit vs red_flags triggered",
            "signal_hit": "+2 points per expected signal present",
            "red_flag_triggered": "-3 points per red flag triggered",
            "max_per_test": 10,
            "min_per_test": 0,
            "fidelity_score": "Sum(test_score * weight) / Sum(max_score * weight) * 100",
            "thresholds": {
                "HIGH_FIDELITY": ">= 80%",
                "ACCEPTABLE": "60-79%",
                "LOW_FIDELITY": "40-59%",
                "FAILED": "< 40%",
            },
        },
    }

    # Save if output path specified
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    # Log
    _log_generation(result)

    return result


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
def _log_generation(result: dict):
    """Log test generation to JSONL."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trigger_type": "blind_test_generation",
        "clone_id": result["clone_id"],
        "clone_name": result["clone_name"],
        "total_tests": result["total_tests"],
        "test_types": {
            t: sum(1 for test in result["tests"] if test["type"] == t)
            for t in TEST_TYPES
        },
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        print("\n=== BLIND TEST GENERATOR v1.0 ===\n")
        persons_dir = AGENTS_ROOT / "persons"
        if not persons_dir.exists():
            print("  No agents/minds/ directory found.")
            sys.exit(1)

        for agent_dir in sorted(persons_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
                continue
            result = generate_blind_test(agent_dir.name)
            status = "OK" if result["total_tests"] > 0 else "SKIP"
            print(f"  [{status}] {result['clone_name']:25s}  {result['total_tests']} tests generated")

    elif len(sys.argv) > 1 and sys.argv[1] != "--help":
        clone_id = sys.argv[1]
        output_path = None
        if "--output" in sys.argv:
            idx = sys.argv.index("--output")
            if idx + 1 < len(sys.argv):
                output_path = sys.argv[idx + 1]

        print(f"\n=== Blind Tests for '{clone_id}' ===\n")
        result = generate_blind_test(clone_id, output_path)

        if result.get("error"):
            print(f"  ERROR: {result['error']}")
            sys.exit(1)

        print(f"  Clone: {result['clone_name']} ({result['clone_type']})")
        print(f"  Tests: {result['total_tests']}")
        print(f"  Domains: {', '.join(result['domains_tested'])}")
        print()

        for test in result["tests"]:
            print(f"  [{test['type']:15s}] {test['test_id']}")
            print(f"    Layer: {test['layer']}")
            print(f"    Prompt: {test['prompt'][:80]}...")
            print(f"    Signals: {len(test['expected_signals'])} | Red flags: {len(test['red_flags'])}")
            print()

        if output_path:
            print(f"  Saved to: {output_path}")

    else:
        print("Usage:")
        print("  python3 blind_test_generator.py <clone_id>                  # Generate tests")
        print("  python3 blind_test_generator.py <clone_id> --output <path>  # Save to file")
        print("  python3 blind_test_generator.py --all                       # All clones")
        sys.exit(1)


if __name__ == "__main__":
    main()
