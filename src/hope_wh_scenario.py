"""Shared setup for the small hope-wh RSA example."""

from __future__ import annotations

from dataclasses import dataclass

from .rsa_model import RSAModel

OBJECTS = ["desire_positive_S", "uncertain_about_S"]
MESSAGES = ["hope_that_S_good", "wonder_what_S", "hope_what_S"]
TRUTH_TABLE = [
    [1, 0],
    [0, 1],
    [1, 0],
]
DESIRE_STATE = OBJECTS.index("desire_positive_S")
MARKED_MESSAGE = MESSAGES.index("hope_what_S")


@dataclass(frozen=True)
class SpeakerAssumption:
    """Parameters used when the listener reasons about a speaker type."""

    label: str
    costs: tuple[float, float, float]
    message_prior: tuple[float, float, float]


NATIVE_ASSUMPTION = SpeakerAssumption(
    label="Native-speaker assumption",
    costs=(0.0, 0.0, 2.0),
    message_prior=(0.49, 0.49, 0.02),
)
L2_ASSUMPTION = SpeakerAssumption(
    label="L2-speaker assumption",
    costs=(0.0, 0.0, 0.5),
    message_prior=(0.40, 0.40, 0.20),
)


def make_model(assumption: SpeakerAssumption, alpha: float = 3.0) -> RSAModel:
    """Build an RSA model from one set of speaker assumptions."""
    return RSAModel(
        objects=OBJECTS,
        messages=MESSAGES,
        truth_table=TRUTH_TABLE,
        alpha=alpha,
        prior_o=(0.5, 0.5),
        prior_m=assumption.message_prior,
        cost_function=lambda: assumption.costs,
    )


def marked_speaker_probability(model: RSAModel) -> float:
    """Return S1(hope_what_S | desire_positive_S)."""
    return model.s1()[DESIRE_STATE][MARKED_MESSAGE]


def cost_sweep(max_cost: float = 3.0, steps: int = 31) -> list[tuple[float, float]]:
    """Vary the marked-message cost while keeping the L2 message prior."""
    rows = []
    for step in range(steps):
        cost = max_cost * step / (steps - 1)
        assumption = SpeakerAssumption("cost sweep", (0.0, 0.0, cost), L2_ASSUMPTION.message_prior)
        rows.append((cost, marked_speaker_probability(make_model(assumption))))
    return rows


def prior_sweep(max_prior: float = 0.40, steps: int = 21) -> list[tuple[float, float]]:
    """Vary the marked-message prior while keeping the L2 cost."""
    rows = []
    for step in range(steps):
        marked_prior = max_prior * step / (steps - 1)
        other_prior = (1.0 - marked_prior) / 2.0
        assumption = SpeakerAssumption("prior sweep", (0.0, 0.0, 0.5), (other_prior, other_prior, marked_prior))
        rows.append((marked_prior, marked_speaker_probability(make_model(assumption))))
    return rows
