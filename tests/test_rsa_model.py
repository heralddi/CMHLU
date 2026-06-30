import pytest

from src.rsa_model import RSAModel


OBJECTS = ["desire_positive_S", "uncertain_about_S"]
MESSAGES = ["hope_that_S_good", "wonder_what_S", "hope_what_S"]
TRUTH_TABLE = [
    [1, 0],
    [0, 1],
    [1, 0],
]


def make_model(costs=(0, 0, 1.0), prior_m=(0.45, 0.45, 0.10)):
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
    model = make_model()

    assert_rows_sum_to_one(model.l0())
    assert_rows_sum_to_one(model.s1())
    assert_rows_sum_to_one(model.l1())


def test_lower_marked_cost_increases_speaker_use():
    high_cost = make_model(costs=(0, 0, 2.0))
    low_cost = make_model(costs=(0, 0, 0.5))

    desire_state = OBJECTS.index("desire_positive_S")
    marked_message = MESSAGES.index("hope_what_S")
    assert low_cost.s1()[desire_state][marked_message] > high_cost.s1()[desire_state][marked_message]


def test_truth_table_shape_is_checked():
    with pytest.raises(ValueError, match="truth_table"):
        RSAModel(OBJECTS, MESSAGES, [[1, 0], [0, 1]], 3.0, [0.5, 0.5], [0.3, 0.3, 0.4], lambda: [0, 0, 1])


def test_message_prior_length_is_checked():
    with pytest.raises(ValueError, match="prior_m"):
        RSAModel(OBJECTS, MESSAGES, TRUTH_TABLE, 3.0, [0.5, 0.5], [0.5, 0.5], lambda: [0, 0, 1])


def test_message_prior_changes_speaker_choice():
    low_prior = make_model(prior_m=(0.49, 0.49, 0.02))
    high_prior = make_model(prior_m=(0.4, 0.4, 0.2))

    desire_state = OBJECTS.index("desire_positive_S")
    marked_message = MESSAGES.index("hope_what_S")
    assert high_prior.s1()[desire_state][marked_message] > low_prior.s1()[desire_state][marked_message]
