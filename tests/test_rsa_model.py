import pytest

from src.hope_wh_scenario import (
    L2_ASSUMPTION,
    NATIVE_ASSUMPTION,
    OBJECTS,
    MESSAGES,
    TRUTH_TABLE,
    make_model,
    marked_speaker_probability,
)
from src.rsa_model import RSAModel
from src.synthetic_pilot import (
    simulate_marked_message_ratings,
    summarize_by_background,
)


def make_test_model(costs=(0, 0, 1.0), prior_m=(0.45, 0.45, 0.10)):
    return RSAModel(
        objects=OBJECTS,
        messages=MESSAGES,
        truth_table=TRUTH_TABLE,
        alpha=3.0,
        prior_o=[0.5, 0.5],
        prior_m=prior_m,
        cost_function=lambda: costs,
    )


def assert_rows_sum_to_one(matrix):
    for row in matrix:
        assert sum(row) == pytest.approx(1.0)


def test_rsa_distributions_are_normalized():
    model = make_test_model()

    assert_rows_sum_to_one(model.l0())
    assert_rows_sum_to_one(model.s1())
    assert_rows_sum_to_one(model.l1())


def test_l2_assumption_increases_marked_speaker_choice():
    native_model = make_model(NATIVE_ASSUMPTION)
    l2_model = make_model(L2_ASSUMPTION)

    assert marked_speaker_probability(l2_model) > marked_speaker_probability(
        native_model
    )


def test_lower_marked_cost_increases_speaker_use():
    high_cost = make_test_model(costs=(0, 0, 2.0))
    low_cost = make_test_model(costs=(0, 0, 0.5))

    marked_message = MESSAGES.index("hope_what_S")
    desire_state = OBJECTS.index("desire_positive_S")
    assert low_cost.s1()[desire_state][marked_message] > high_cost.s1()[
        desire_state
    ][marked_message]


def test_truth_table_shape_is_checked():
    with pytest.raises(ValueError, match="truth_table"):
        RSAModel(
            OBJECTS,
            MESSAGES,
            [[1, 0], [0, 1]],
            3.0,
            [0.5, 0.5],
            [0.3, 0.3, 0.4],
            lambda: [0, 0, 1],
        )


def test_message_prior_length_is_checked():
    with pytest.raises(ValueError, match="prior_m"):
        RSAModel(
            OBJECTS,
            MESSAGES,
            TRUTH_TABLE,
            3.0,
            [0.5, 0.5],
            [0.5, 0.5],
            lambda: [0, 0, 1],
        )


def test_negative_prior_is_rejected():
    with pytest.raises(ValueError, match="prior_m"):
        make_test_model(prior_m=(0.5, 0.6, -0.1))


def test_zero_prior_is_rejected():
    with pytest.raises(ValueError, match="prior_o"):
        RSAModel(
            OBJECTS,
            MESSAGES,
            TRUTH_TABLE,
            3.0,
            [0, 0],
            [0.3, 0.3, 0.4],
            lambda: [0, 0, 1],
        )


def test_cost_function_length_is_checked():
    model = make_test_model(costs=(0, 1))
    with pytest.raises(ValueError, match="cost_function"):
        model.s1()


def test_message_prior_changes_speaker_choice():
    low_prior = make_test_model(prior_m=(0.49, 0.49, 0.02))
    high_prior = make_test_model(prior_m=(0.4, 0.4, 0.2))

    marked_message = MESSAGES.index("hope_what_S")
    desire_state = OBJECTS.index("desire_positive_S")
    assert high_prior.s1()[desire_state][marked_message] > low_prior.s1()[
        desire_state
    ][marked_message]


def test_prior_sweep_moves_in_expected_direction():
    from src.hope_wh_scenario import prior_sweep

    rows = prior_sweep()
    assert rows[0][1] < rows[-1][1]


def test_synthetic_pilot_is_deterministic_and_l2_is_higher():
    rows = simulate_marked_message_ratings(participants_per_condition=8, seed=5)
    repeat_rows = simulate_marked_message_ratings(
        participants_per_condition=8,
        seed=5,
    )
    summary = summarize_by_background(rows)

    assert rows == repeat_rows
    assert summary["l2"] > summary["native"]
