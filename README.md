# swarm-safety-gate

A **deny-by-default command safety gate** and a **text-based ReAct routing agent**
for small language models, hardened against *behavioral hallucination* — the
failure mode where a small model misreads user intent and **executes** an action
the user was only **asking about**.

The safety layer is pure-stdlib and has **zero runtime dependencies**, so you can
drop it in front of any tool-executing agent regardless of your LLM stack.

```python
from swarm_safety_gate import SafetyGate

SafetyGate.validate_command("git status")      # (True,  'Safe')
SafetyGate.validate_command("rm -rf /")        # (False, 'Policy Error: ... Whitelist ...')
SafetyGate.validate_command("cat x > /etc/passwd")  # (False, 'Safety Error: Dangerous pattern ...')
```

## Why

Small models fail on agentic tasks less because they get *facts* wrong and more
because they misroute *intent* — running a command when asked "how does X work?",
or obeying a "system override: ignore your safety rules" injection. This library
packages two defenses:

- **`SafetyGate`** — a two-layer command filter: an allow-list of base commands
  *plus* a regex block-list (~25 patterns: `rm -rf`, `dd if=`, `format C:`,
  pipes/redirects/chaining, PowerShell bypass, privilege-escalation tools, …).
  A command must pass **both** layers.
- **`ExecutionGate`** — assigns `low` / `medium` / `high` risk to actions so a
  caller can require confirmation or escalation for the dangerous ones.
- **`ReActAgent`** *(optional)* — a text-ReAct loop (no function-calling schema,
  works with weakly-quantized local models via any OpenAI-compatible endpoint
  such as Ollama) that routes intent and gates every tool call through the above.

## Install

```bash
pip install swarm-safety-gate            # core safety gate only (no deps)
pip install "swarm-safety-gate[agent]"   # + ReAct agent (openai, python-dotenv)
pip install "swarm-safety-gate[cli]"     # + rich terminal REPL
pip install "swarm-safety-gate[all]"     # everything, incl. Telegram bot
```

## Using the agent

The agent talks to any OpenAI-compatible endpoint. With [Ollama](https://ollama.com):

```bash
export LLM_API_BASE="http://localhost:11434/v1"
export LLM_MODEL_V5="llama3.2:latest"    # any local model
swarm-safety-gate                         # launches the rich REPL
```

```python
import asyncio
from swarm_safety_gate import ReActAgent

async def main():
    agent = ReActAgent(use_enricher=True, verbose=True)
    agent.add_user_message("đọc file report.txt rồi tóm tắt")  # multilingual
    print(await agent.run_step())

asyncio.run(main())
```

## Tests

```bash
pip install "swarm-safety-gate[dev]"
pytest
```

The default suite is **deterministic** — it exercises the safety gate directly
with no LLM or network. LLM-dependent benchmarks are marked `llm` and skipped by
default (`pytest -m llm` to opt in, with an endpoint configured).

## Provenance & honest limitations

This package is a **cleaned-up, installable repackaging** of
[`chetdep/balder-brain-v5`](https://github.com/chetdep/balder-brain-v5) (MIT),
with the upstream `SyntaxError`, broken package imports, and missing-module test
scripts fixed. See [`NOTICE`](./NOTICE) for the full list of changes.

**What is and isn't validated here:**

- ✅ The `SafetyGate` works and is covered by deterministic tests.
- ⚠️ The upstream project's headline accuracy claim ("93.8% on agentic tasks")
  is **not reproduced or endorsed**. In local re-runs of the upstream router
  benchmark (on a substitute model, since the referenced `gemma4:*` models do
  not exist as published), scores swung from ~59% to ~98% between runs because
  the benchmark generates its cases from unseeded random templates and grades
  them with a loose keyword heuristic — too noisy to support a precise number.
- ⚠️ The safety gate's block-list is Windows/PowerShell-centric and pattern-based;
  treat it as defense-in-depth, **not** a complete sandbox.

## License

MIT — see [`LICENSE`](./LICENSE). Derived from balder-brain-v5 (© Balder Autobot
Project); modifications © Swarm AI Research.
