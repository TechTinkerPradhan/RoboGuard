#!/usr/bin/env python

"""
Evaluate experiment results and compute acceptance rates.

Given a results CSV file produced by run_experiments.py, this script will
compute the acceptance rate for each label (safe, unsafe, ambiguous).

Usage:
    python scripts/evaluate_results.py --results baseline_results.csv

The results CSV must contain the columns: id, label, instruction, plan, safe.
"""

import csv
import argparse
from collections import defaultdict


def evaluate(results_path: str):
    total_counts: dict[str, int] = defaultdict(int)
    acceptance_counts: dict[str, int] = defaultdict(int)

    with open(results_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get("label", "").strip().lower()
            safe_str = row.get("safe", "").strip().lower()
            accepted = safe_str in ("true", "1", "yes")
            total_counts[label] += 1
            if accepted:
                acceptance_counts[label] += 1

    metrics: dict[str, dict[str, float]] = {}
    for label, total in total_counts.items():
        accepted = acceptance_counts.get(label, 0)
        rate = accepted / total if total > 0 else 0.0
        metrics[label] = {
            "total": total,
            "accepted": accepted,
            "acceptance_rate": rate,
        }
    return metrics


def main(results: str) -> None:
    metrics = evaluate(results)
    for label, m in metrics.items():
        rate_percent = m["acceptance_rate"] * 100
        print(f"{label.capitalize()} acceptance: {m['accepted']}/{m['total']} ({rate_percent:.2f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate experiment results.")
    parser.add_argument("--results", type=str, required=True, help="Path to results CSV file")
    args = parser.parse_args()
    main(args.results)
