"""A small Rational Speech Act model used in the hope-wh notebook.

The code stays deliberately compact. It is meant for exploratory modeling:
messages map onto possible speaker states, and costs / message priors can be
changed to see how a pragmatic listener's inference shifts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Callable, Sequence


NumberList = Sequence[float]
Matrix = list[list[float]]


def normalize(values: NumberList) -> list[float]:
    """Normalize a list of numbers, returning zeros if the total is zero."""
    total = sum(values)
    if total == 0:
        return [0.0 for _ in values]
    return [float(value) / total for value in values]


def normalize_rows(matrix: Sequence[NumberList]) -> Matrix:
    """Normalize each row in a matrix."""
    return [normalize(row) for row in matrix]


@dataclass
class RSAModel:
    """A minimal RSA model with object priors, message priors, and message costs."""

    objects: Sequence[str]
    messages: Sequence[str]
    truth_table: Sequence[Sequence[float]]
    alpha: float
    prior_o: NumberList
    prior_m: NumberList
    cost_function: Callable[[], NumberList]

    def __post_init__(self) -> None:
        self.truth_table = [[float(cell) for cell in row] for row in self.truth_table]
        expected_shape = (len(self.messages), len(self.objects))
        actual_shape = (len(self.truth_table), len(self.truth_table[0]) if self.truth_table else 0)
        if actual_shape != expected_shape:
            raise ValueError("truth_table must have shape (number of messages, number of objects)")
        if len(self.prior_o) != len(self.objects):
            raise ValueError("prior_o must have one value for each object")
        if len(self.prior_m) != len(self.messages):
            raise ValueError("prior_m must have one value for each message")

        self.prior_o = normalize(self.prior_o)
        self.prior_m = normalize(self.prior_m)

    def l0(self) -> Matrix:
        """Literal listener P(object | message)."""
        weighted_truth = []
        for row in self.truth_table:
            weighted_truth.append([truth * prior for truth, prior in zip(row, self.prior_o)])
        return normalize_rows(weighted_truth)

    def s1(self) -> Matrix:
        """Pragmatic speaker P(message | object)."""
        costs = list(self.cost_function())
        if len(costs) != len(self.messages):
            raise ValueError("cost_function must return one cost for each message")

        literal_listener = self.l0()
        rows_by_object = []
        for object_index in range(len(self.objects)):
            scores = []
            for message_index in range(len(self.messages)):
                l0_prob = literal_listener[message_index][object_index]
                utility = log(l0_prob + 1e-12) - costs[message_index]
                scores.append(exp(self.alpha * utility) * self.prior_m[message_index])
            rows_by_object.append(normalize(scores))
        return rows_by_object

    def l1(self) -> Matrix:
        """Pragmatic listener P(object | message)."""
        speaker = self.s1()
        rows_by_message = []
        for message_index in range(len(self.messages)):
            scores = []
            for object_index in range(len(self.objects)):
                scores.append(speaker[object_index][message_index] * self.prior_o[object_index])
            rows_by_message.append(normalize(scores))
        return rows_by_message
