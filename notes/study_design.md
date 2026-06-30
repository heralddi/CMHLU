# Sketch for a small judgment study

This is a first-pass design note. It connects the toy RSA model to a possible
psycholinguistic follow-up, not to a finalized preregistration.

## Question

Do listeners expect a marked `hope-wh` sentence to be more likely when the
speaker is described as an advanced L2 English speaker rather than a native
English speaker?

## Participants

A small pilot could start with native English listeners. The speaker-background
manipulation would be in the prompt, for example by describing the speaker as a
native English speaker or as an advanced L2 English speaker.

## Design

Possible factors:

- speaker background: native English speaker vs. L2 English speaker
- sentence type: standard declarative complement vs. marked wh-complement
- predicate type: `hope`, `fear`, `wonder`, and a control predicate such as
  `know`

## Item template

| Slot | Example value |
| --- | --- |
| predicate | `hope`, `fear`, `wonder`, `know` |
| event noun | `meeting`, `exam`, `interview`, `trip` |
| positive outcome | `goes well`, `turns out okay`, `ends smoothly` |
| wh-frame | `what will happen at the meeting` |

Example item pair:

| Condition | Example |
| --- | --- |
| Standard declarative complement | `I hope that the meeting goes well.` |
| Marked wh-complement | `I hope what will happen at the meeting.` |
| Standard embedded wh-control | `I wonder what will happen at the meeting.` |

## Measures

Participants could rate:

- how acceptable or natural the sentence sounds
- how likely this speaker would be to say the sentence
- how likely the speaker is expressing a positive desire
- how likely the speaker is asking for information

## Exclusion criteria for a pilot

Possible pilot exclusions:

- participants who fail a simple attention check
- participants who report not being fluent enough in English for the task
- participants who give the same response on nearly every trial
- items with obvious wording mistakes after a small pretest

## Predictions

The current RSA model predicts a speaker-choice effect: `hope_what_S` should be
judged more likely under an L2-speaker description than under a native-speaker
description. It does not yet make a strong prediction that the final listener
interpretation of `hope_what_S` changes, because the current truth table maps
the marked message directly to the positive-desire state.

## Model connection

In the RSA model, a listener's assumptions about speaker background are
represented with message costs and message priors. If listeners are more willing
to treat `hope what S` as a plausible utterance under the L2-speaker prompt,
that would match the direction of the toy model.

## Current limits

There is no human data yet. The current parameters are hand-set, and the marked
construction is represented with a very simple message-state mapping. A pilot
would mainly test whether this modeling direction is worth developing further.
