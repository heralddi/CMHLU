"""Synthetic pilot data helpers for the hope-wh RSA example."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from statistics import mean

from .hope_wh_scenario import (
    L2_ASSUMPTION,
    NATIVE_ASSUMPTION,
    make_model,
    marked_speaker_probability,
)


@dataclass(frozen=True)
class SyntheticRating:
    """One simulated judgment for the marked hope-wh item."""

    participant: int
    speaker_background: str
    rating: float


def _clip_rating(value: float) -> float:
    return min(7.0, max(1.0, value))


def simulate_marked_message_ratings(
    participants_per_condition: int = 24,
    seed: int = 17,
) -> list[SyntheticRating]:
    """Simulate plausibility ratings for the marked utterance.

    The simulation maps the RSA speaker-choice probability onto a 1--7 rating
    scale and adds small seeded noise. It is only a workflow check; it is not
    synthetic evidence for the theory.
    """
    rng = Random(seed)
    assumptions = [NATIVE_ASSUMPTION, L2_ASSUMPTION]
    rows: list[SyntheticRating] = []

    for assumption in assumptions:
        probability = marked_speaker_probability(make_model(assumption))
        expected_rating = 2.0 + 12.0 * probability
        label = "native" if assumption is NATIVE_ASSUMPTION else "l2"

        for participant in range(participants_per_condition):
            noise = rng.gauss(0.0, 0.35)
            rows.append(
                SyntheticRating(
                    participant=participant,
                    speaker_background=label,
                    rating=round(_clip_rating(expected_rating + noise), 2),
                )
            )

    return rows


def summarize_by_background(rows: list[SyntheticRating]) -> dict[str, float]:
    """Return mean ratings by speaker-background condition."""
    backgrounds = sorted({row.speaker_background for row in rows})
    return {
        background: mean(
            row.rating for row in rows if row.speaker_background == background
        )
        for background in backgrounds
    }
