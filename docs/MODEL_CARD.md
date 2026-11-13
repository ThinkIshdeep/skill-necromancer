# Model and simulator card — Skill Necromancer

## Intended use

A narrow adaptive-practice tool that tracks concept estimates and checks Gaussian-elimination row operations exactly.

## Implemented methods

- Generated practice for signs, scaling and elimination
- Bayesian knowledge-tracing updates with slip/guess parameters
- Lowest-estimated-mastery question selection
- Exact rational-arithmetic row-operation validation
- Hints, recall triggers and attempt history

Some projects use deterministic simulators and rules rather than trained neural models. Those distinctions are retained in this card and the source.

## Evaluation

See `docs/EXPERIMENTS.md` and the machine-readable reports. No pretrained foundation-model weights or real-world efficacy certification are included. Parameters, splits and synthetic generators are visible in source.

## Limitations

Small authored question generator, BKT estimates, exact row checks. No measured human learning gains or semester-sized item bank.

## Extensions not implemented in this release

- Validated misconception classification and spaced scheduling
- Consented student studies and delayed learning assessments
