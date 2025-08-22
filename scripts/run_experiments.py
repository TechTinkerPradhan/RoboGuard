#!/usr/bin/env python
"""
Run experiments on a dataset of instructions with different safety modes.

This script is a starter template for evaluating an LLM-controlled robot with
optional safety guardrails.

Usage example:
    python scripts/run_experiments.py --dataset data/experiment_scenarios.csv --mode baseline

Modes:
  baseline   - no safety filtering; execute the raw plan from your planner.
  chip       - apply SafetyChipLite on the plan (requires LTL rules).
  roboguard  - apply RoboGuard on the plan (requires context update).
  combined   - apply both SafetyChipLite and RoboGuard.

Before using this script you need to implement your own planner that
converts natural-language instructions into a sequence of actions.  You
may also need to provide a scene graph and safety rules for RoboGuard
and SafetyChipLite.
"""

import csv
import argparse
from typing import List, Dict, Any

# Import safety modules if available
try:
    from roboguard.roboguard import RoboGuard
    from roboguard.safety_chip_lite import SafetyChipLite
except ImportError:
    RoboGuard = None  # type: ignore
    SafetyChipLite = None  # type: ignore


def load_dataset(path: str) -> List[Dict[str, str]]:
    """Load the CSV dataset into a list of dicts."""
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def dummy_planner(instruction: str) -> List[str]:
    """
    Dummy planner that returns an empty plan.  Replace this with your
    call to an LLM-based planner (e.g. SPINE or your own implementation).
    """
    return []


def main(dataset: str, mode: str, output: str, graph: str | None = None) -> None:
    data = load_dataset(dataset)
    results: List[Dict[str, Any]] = []

    # Instantiate safety modules based on the selected mode
    chip: SafetyChipLite | None = None
    rg: RoboGuard | None = None

    if mode in ("chip", "combined") and SafetyChipLite is not None:
        # TODO: Define your LTL rules here.  For example:
        # ltl_rules = ["G(! (use_knife & near_person))", "G(! (mix_bleach & X mix_ammonia))"]
        ltl_rules: List[str] = []
        chip = SafetyChipLite(ltl_rules)

    if mode in ("roboguard", "combined") and RoboGuard is not None:
        rg = RoboGuard()
        if graph is not None:
            # TODO: Update the RoboGuard context with your scene graph
            with open(graph, "r", encoding="utf-8") as gf:
                scene_graph_json = gf.read()
            rg.update_context(scene_graph_json)

    for row in data:
        instr = row["instruction"]
        plan: List[str] = dummy_planner(instr)

        # Determine safety based on the selected mode
        safe = True
        if mode == "baseline":
            safe = True
        elif mode == "chip" and chip is not None:
            safe = chip.validate(plan)
        elif mode == "roboguard" and rg is not None:
            is_safe, _ = rg.validate_plan(plan)  # type: ignore[arg-type]
            safe = is_safe
        elif mode == "combined":
            safe_chip = chip.validate(plan) if chip is not None else True
            safe_rg = True
            if rg is not None:
                is_safe, _ = rg.validate_plan(plan)  # type: ignore[arg-type]
                safe_rg = is_safe
            safe = safe_chip and safe_rg

        results.append({
            "id": row.get("id"),
            "label": row.get("label"),
            "instruction": instr,
            "plan": " ".join(plan),
            "safe": safe,
        })

    # Write results to CSV
    with open(output, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "label", "instruction", "plan", "safe"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} results to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run experiments on a dataset of instructions.")
    parser.add_argument("--dataset", type=str, required=True, help="Path to the CSV file of scenarios.")
    parser.add_argument("--mode", type=str, default="baseline", choices=["baseline", "chip", "roboguard", "combined"],
                        help="Select which safety filter(s) to apply.")
    parser.add_argument("--output", type=str, default="results.csv", help="Path to the output results CSV.")
    parser.add_argument("--graph", type=str, default=None,
                        help="Path to the scene graph JSON file for RoboGuard (if applicable).")
    args = parser.parse_args()
    main(args.dataset, args.mode, args.output, args.graph)
