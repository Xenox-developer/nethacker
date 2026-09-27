# Tactical lookahead experiment

This directory contains an isolated implementation for the participant bot.
It does not modify or replace the saved champion by itself. The official evolve
container installs it into a candidate and evaluates that candidate normally.

`planner.py` searches sequences of three player actions and enemy responses,
using deterministic nominal and adverse estimates. A narrow adapter considers
only supported movement/melee decisions, retains urgent actions, and requires
a meaningful estimated reduction in harm before overriding the existing bot.
The model uses observed terrain and public species data, with approximate
health/damage/speed assumptions. Its forecasts are not calibrated probabilities.

To stage an experiment without interrupting an active cycle:

```sh
uv run --no-dev python scripts/participant_lab.py request \
  participant_extensions/tactical_lookahead/REQUEST.md \
  --name tactical-lookahead --assets participant_extensions/tactical_lookahead
```

The request and assets are frozen and assigned to the next fresh input tree.
Only run this once per intended experiment. The installer belongs inside that
official mutator workspace; never run it against a champion or active snapshot.
All fully scored candidates are published by the authorized autopilot, while
champion promotion still requires full Public improvement and fresh validation.
