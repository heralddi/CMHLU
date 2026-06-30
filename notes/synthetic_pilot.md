# Synthetic pilot simulation

This file is written by `python scripts/simulate_pilot.py`.
It uses seeded synthetic ratings to check the workflow for a future
judgment study. The numbers are not human data.

## Mean marked-message plausibility rating

| Speaker background | Mean rating |
| --- | ---: |
| l2 | 3.24 |
| native | 1.93 |

## Interpretation

The synthetic L2 condition is higher because the toy RSA model gives
the marked `hope_what_S` message a lower cost and higher prior under
the L2-speaker assumption. This is only a design check before using
real participant judgments.
