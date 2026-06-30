# Model assumptions

This note keeps the toy model's assumptions explicit. It is not a claim that
these values are empirically correct.

## States

The model currently has two possible speaker states:

- `desire_positive_S`: the speaker wants a positive outcome.
- `uncertain_about_S`: the speaker is primarily seeking information.

## Messages

The model compares three messages:

- `hope_that_S_good`: a standard way to express a positive desire.
- `wonder_what_S`: a standard way to express uncertainty or information
  seeking.
- `hope_what_S`: the marked target form.

## Truth table

The truth table is deliberately simple. It treats `hope_that_S_good` and
`hope_what_S` as compatible with the positive-desire state, and
`wonder_what_S` as compatible with the uncertainty state.

This makes the current listener interpretation mostly deterministic. For that
reason, the most useful first result is the speaker-choice quantity
`S1(hope_what_S | desire_positive_S)`, not a strong claim that the final
listener interpretation changes.

## Costs

Costs represent how marked or difficult a message is assumed to be for the
modeled speaker. In the native-speaker assumption, the marked `hope_what_S`
message has a higher cost. In the L2-speaker assumption, the same message has a
lower cost.

## Message priors

Message priors represent how available a message is before the speaker chooses
an utterance for a specific state. The L2-speaker assumption gives the marked
message a higher prior than the native-speaker assumption.

## What should change next

The hand-set costs and priors should eventually be replaced by values motivated
by acceptability judgments, corpus counts, or a small production/interpretation
pilot. Until then, the model is best read as a sensitivity check.
