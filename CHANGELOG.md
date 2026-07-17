# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- PEP 561 `py.typed` marker so downstream users get the shipped type hints.
- `CONTRIBUTING.md`, issue/PR templates.

## [0.1.0] - 2026-07-03

First release. A cleaned-up, installable repackaging of
[`chetdep/balder-brain-v5`](https://github.com/chetdep/balder-brain-v5) (MIT).

### Added
- `SafetyGate` / `ExecutionGate`: zero-dependency, deny-by-default command safety
  layer (allow-list + regex block-list + risk scoring).
- Optional `ReActAgent` (text-ReAct loop for OpenAI-compatible endpoints) behind
  the `[agent]` extra; `[cli]` REPL and `[telegram]` bot extras.
- Deterministic pytest suite for the safety layer.
- Seeded, reproducible safety-gate benchmark (`benchmarks/router_benchmark.py`).
- GitHub Actions CI across Python 3.9–3.13.

### Fixed (relative to upstream balder-brain-v5)
- `SyntaxError` (IndentationError) in `agent_core.py` that prevented the core
  module from importing at all.
- Whitelist case-sensitivity bug: mixed-case entries (`Get-Content`, etc.) were
  compared against a lower-cased command and so could never match.
- Broken `from Core.X` absolute imports → intra-package relative imports.
- `bot.py` imported a non-existent `agent_brain_v3` module → rewired onto the
  packaged `ReActAgent`.

### Changed
- Restructured into a `src/`-layout installable package with `pyproject.toml`.
- Added cross-platform dangerous-command patterns (shutdown/reboot/halt/poweroff,
  shred, wipefs, chown, doas, killall, crontab, fork bomb).

### Note
- Upstream accuracy claims (e.g. "93.8%") are **not** reproduced or endorsed. See
  `README.md` and `NOTICE`.

[Unreleased]: https://github.com/swarm-ai-research/swarm-safety-gate/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/swarm-ai-research/swarm-safety-gate/releases/tag/v0.1.0
