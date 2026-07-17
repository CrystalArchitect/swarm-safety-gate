# Contributing

Thanks for your interest in `swarm-safety-gate`.

## Development setup

```bash
git clone https://github.com/swarm-ai-research/swarm-safety-gate
cd swarm-safety-gate
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,agent,cli]"
pytest
```

## Ground rules

- **The safety core stays dependency-free.** `safety.py` (and anything imported
  by `swarm_safety_gate/__init__.py` at import time) must not import third-party
  packages. LLM/CLI/Telegram code belongs behind the optional extras and must be
  imported lazily.
- **Tests are deterministic by default.** Anything needing an LLM or network must
  be marked `@pytest.mark.llm` (skipped unless you run `pytest -m llm` with an
  endpoint configured). The default `pytest` run must pass with no network.
- **Every safety-gate change needs a test.** New allow-list entries or dangerous
  patterns must come with a case in `tests/test_safety_gate.py`.

## Adding a dangerous pattern

1. Add the regex to `SafetyGate.DANGEROUS_PATTERNS` in `src/swarm_safety_gate/safety.py`.
2. Add a parametrized case to `test_new_dangerous_patterns_denied` (or a nearby
   test) proving a whitelisted base command carrying that token is blocked.
3. Run `python benchmarks/router_benchmark.py --seed 0 --n 200` — it must still
   exit 0 (no dangerous case leaks) and not newly block a legitimately-safe case.

## Pull requests

- Keep PRs focused; update `CHANGELOG.md` under `[Unreleased]`.
- CI (Python 3.9–3.13) must be green.
- By contributing you agree your work is licensed under the project's MIT license.

## Scope & honesty

This project deliberately does **not** re-assert upstream accuracy claims. Please
don't add benchmark numbers to the docs unless they are produced by a **seeded,
reproducible** procedure and clearly state the model and method.
