## Summary

<!-- What does this change and why? -->

## Checklist

- [ ] `pytest` passes locally (default suite, no network)
- [ ] Safety-gate changes include a test in `tests/test_safety_gate.py`
- [ ] `python benchmarks/router_benchmark.py --seed 0 --n 200` still exits 0
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] The safety core (`safety.py`) remains dependency-free
