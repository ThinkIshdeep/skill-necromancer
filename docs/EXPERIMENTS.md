# Experiments and reproduction

Run `python scripts/evaluate_all.py` from this repository. The report is written to `reports/evaluation-results.json`. This executes real calculations; model quality is separate from test success.

## Recorded baseline

```json
{
  "checks": {
    "correct_answer_raises_posterior": true,
    "exact_row_check": true,
    "rational_values_preserved": true
  },
  "note": "Mathematical/BKT regression checks. Synthetic histories do not prove learning gains."
}
```

## Interpretation

Small authored question generator, BKT estimates, exact row checks. No measured human learning gains or semester-sized item bank.

The raw reports describe whether measurements are synthetic benchmarks, controlled regression fixtures or invariants. Do not interpret regression-fixture accuracy as a held-out real-world score. Preserve seeds and splits when comparing changes.
