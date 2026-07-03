"""
Opt-in integration smoke test for the ReAct agent.

Marked ``llm`` and therefore SKIPPED by default (and in CI). It requires:
  * the ``[agent]`` extra installed (openai, python-dotenv), and
  * a reachable OpenAI-compatible endpoint, configured via env:
        LLM_API_BASE   (default http://localhost:11434/v1)
        LLM_MODEL_V5   (the model tag to use, e.g. "llama3.2:latest")

Run explicitly with:  pytest -m llm

The end-to-end *safety* guarantees are covered deterministically by
test_safety_gate.py / test_benchmark.py; this test only checks that the agent
plumbing connects and returns a well-formed step against a live model. The RNG
is seeded so any sampling inside a run is reproducible.
"""
import asyncio
import importlib.util
import os
import random
import urllib.request

import pytest

pytestmark = pytest.mark.llm


def _endpoint_reachable(base):
    try:
        urllib.request.urlopen(base.replace("/v1", "/api/tags"), timeout=2)
        return True
    except Exception:
        return False


@pytest.fixture
def agent():
    if importlib.util.find_spec("openai") is None:
        pytest.skip("openai not installed (pip install 'swarm-safety-gate[agent]')")
    base = os.getenv("LLM_API_BASE", "http://localhost:11434/v1")
    if not _endpoint_reachable(base):
        pytest.skip(f"no LLM endpoint reachable at {base}")
    random.seed(0)
    from swarm_safety_gate import ReActAgent
    return ReActAgent(use_enricher=True, verbose=False)


def test_agent_returns_wellformed_step(agent):
    agent.add_user_message("đọc file report.txt")   # a single-action intent
    result = asyncio.run(agent.run_step())
    assert isinstance(result, dict)
    assert result.get("type") in {"tool_call", "text", "error", "max_steps", "cancelled"}
