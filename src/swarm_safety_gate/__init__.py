"""
swarm-safety-gate
=================

A deny-by-default command safety gate and text-ReAct routing agent for small
language models, hardened against *behavioral hallucination* — where a small
model misreads user intent and executes an action the user only asked about.

The safety layer (``SafetyGate`` / ``ExecutionGate``) is pure-stdlib and has
**no dependencies**, so it can be imported and used on its own:

    >>> from swarm_safety_gate import SafetyGate
    >>> SafetyGate.validate_command("git status")
    (True, 'Safe')
    >>> ok, reason = SafetyGate.validate_command("rm -rf /")
    >>> ok
    False

The optional ReAct agent requires the ``[agent]`` extra (openai, python-dotenv).
It is exposed lazily so that importing this package never pulls heavy deps.

Derived from chetdep/balder-brain-v5 (MIT). See NOTICE.
"""

from .safety import SafetyGate, ExecutionGate

__version__ = "0.1.0"

__all__ = ["SafetyGate", "ExecutionGate", "ReActAgent"]


def __getattr__(name):
    # Lazy import so `import swarm_safety_gate` works without the [agent] extra.
    if name == "ReActAgent":
        from .agent_core import ReActAgent
        return ReActAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
