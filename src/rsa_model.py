"""Small Rational Speech Act helpers for the hope-wh notebook.

The model is intentionally compact: it is meant to make a few assumptions
about message meanings, costs, and priors easy to inspect rather than to be a
full account of embedded questions.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Callable, Sequence

NumberList = Sequence[float]
Matrix = list[list[float]]


def _as_probability_values(values: NumberList, name: str) -> list[float]:
    """Convert and validate a list that will be used as a probability vector."""
    converted = [float(value) for value in values]
    if not converted:
        raise ValueError(f"{name} must not be empty")
    if any(not isfinite(value) for value in converted):
        raise ValueError(f"{name} must contain only finite values")
    if any(value < 0 for value in converted):
        raise ValueError(f"{name} must not contain negative values")
    if sum(converted) == 0:
        raise ValueError(f"{name} must contain at least one positive value")
    return converted


def normalize(values: NumberList, name: str = "values") -> list[float]:
    """Normalize a non-negative list of numbers into a probability vector."""
    converted = _as_probability_values(values, name)
    total = sum(converted)
    return [value / total for value in converted]


def normalize_scores(values: NumberList) -> list[float]:
    """Normalize model scores that are already known to be non-negative."""
    total = sum(values)
    if total == 0:
        return [0.0 for _ in values]
    return [float(value) / total for value in values]


def normalize_rows(matrix: Sequence[NumberList]) -> Matrix:
    """Normalize each row in a matrix of model scores."""
    return [normalize_scores(row) for row in matrix]


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
        if self.alpha <= 0 or not isfinite(self.alpha):
            raise ValueError("alpha must be a positive finite value")

        self.truth_table = [[float(cell) for cell in row] for row in self.truth_table]
        expected_shape = (len(self.messages), len(self.objects))
        actual_shape = (len(self.truth_table), len(self.truth_table[0]) if self.truth_table else 0)
        if actual_shape != expected_shape:
            raise ValueError("truth_table must have shape (number of messages, number of objects)")
        for row in self.truth_table:
            if len(row) != len(self.objects):
                raise ValueError("truth_table rows must all match the number of objects")
            if any(cell < 0 for cell in row):
                raise ValueError("truth_table must not contain negative values")

        if len(self.prior_o) != len(self.objects):
            raise ValueError("prior_o must have one value for each object")
        if len(self.prior_m) != len(self.messages):
            raise ValueError("prior_m must have one value for each message")

        self.prior_o = normalize(self.prior_o, "prior_o")
        self.prior_m = normalize(self.prior_m, "prior_m")

    def l0(self) -> Matrix:
        """Literal listener P(object | message)."""
        weighted_truth = []
        for row in self.truth_table:
            weighted_truth.append([truth * prior for truth, prior in zip(row, self.prior_o)])
        return normalize_rows(weighted_truth)

    def s1(self) -> Matrix:
        """Pragmatic speaker P(message | object)."""
        costs = [float(cost) for cost in self.cost_function()]
        if len(costs) != len(self.messages):
            raise ValueError("cost_function must return one cost for each message")
        if any(not isfinite(cost) for cost in costs):
            raise ValueError("cost_function must return finite costs")

        literal_listener = self.l0()
        rows_by_object = []
        for object_index in range(len(self.objects)):
            scores = []
            for message_index in range(len(self.messages)):
                l0_prob = literal_listener[message_index][object_index]
                utility = log(l0_prob + 1e-12) - costs[message_index]
                scores.append(exp(self.alpha * utility) * self.prior_m[message_index])
            rows_by_object.append(normalize_scores(scores))
        return rows_by_object

    def l1(self) -> Matrix:
        """Pragmatic listener P(object | message)."""
        speaker = self.s1()
        rows_by_message = []
        for message_index in range(len(self.messages)):
            scores = []
            for object_index in range(len(self.objects)):
                scores.append(speaker[object_index][message_index] * self.prior_o[object_index])
            rows_by_message.append(normalize_scores(scores))
        return rows_by_message
