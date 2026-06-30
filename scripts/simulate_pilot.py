"""Write a small synthetic-pilot summary for the README notes."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.synthetic_pilot import simulate_marked_message_ratings, summarize_by_background

OUTPUT_PATH = PROJECT_ROOT / "notes" / "synthetic_pilot.md"


def main() -> None:
    rows = simulate_marked_message_ratings()
    summary = summarize_by_background(rows)

    lines = [
        "# Synthetic pilot simulation",
        "",
        "This file is written by `python scripts/simulate_pilot.py`.",
        "It uses seeded synthetic ratings to check the workflow for a future",
        "judgment study. The numbers are not human data.",
        "",
        "## Mean marked-message plausibility rating",
        "",
        "| Speaker background | Mean rating |",
        "| --- | ---: |",
    ]
    for background, value in summary.items():
        lines.append(f"| {background} | {value:.2f} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The synthetic L2 condition is higher because the toy RSA model gives",
            "the marked `hope_what_S` message a lower cost and higher prior under",
            "the L2-speaker assumption. This is only a design check before using",
            "real participant judgments.",
        ]
    )
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
