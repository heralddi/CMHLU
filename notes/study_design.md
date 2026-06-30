# Sketch for a small judgment study

This is a first-pass design note. It is meant to connect the toy RSA model to a possible psycholinguistic follow-up, not to serve as a preregistration.

## Question

Do listeners interpret a marked `hope-wh` sentence differently when they think the speaker is a native English speaker versus an L2 English speaker?

## Participants

A small pilot could start with native English listeners. The speaker background manipulation would be in the prompt, for example by describing the speaker as a native English speaker or as an advanced L2 English speaker.

## Design

Possible factors:

- speaker background: native English speaker vs. L2 English speaker
- sentence type: standard declarative complement vs. marked wh-complement
- predicate type: `hope`, `fear`, `wonder`, and possibly a control predicate such as `know`

Example item pair:

- Standard: `I hope that the meeting goes well.`
- Marked: `I hope what will happen at the meeting.`

## Measures

Participants could rate:

- how acceptable or natural the sentence sounds
- how likely the speaker is expressing a positive desire
- how likely the speaker is asking for information

## Model connection

In the RSA model, a listener's assumptions about speaker background are represented with message costs and message priors. If listeners are more willing to infer a coherent desire from `hope what S` under the L2-speaker prompt, that would match the direction of the toy model.

## Current limits

There is no human data yet. The current parameters are hand-set, and the marked construction is represented with a very simple message-state mapping. A pilot would mainly test whether this modeling direction is worth developing further.
