"""
Deterministic checks for the reproducible safety-gate benchmark.

These run in CI (no LLM): they assert the benchmark blocks every dangerous case
and that its result is identical across runs with the same seed — the property
the upstream (unseeded) benchmark lacked.
"""
import importlib.util
import pathlib

_BENCH = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "router_benchmark.py"
_spec = importlib.util.spec_from_file_location("router_benchmark", _BENCH)
router_benchmark = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(router_benchmark)


def test_no_dangerous_case_leaks():
    assert router_benchmark.run(seed=0, n=200) is True


def test_benchmark_cases_are_reproducible():
    import random
    a = router_benchmark.build_cases(random.Random(0), 100)
    b = router_benchmark.build_cases(random.Random(0), 100)
    assert a == b, "same seed must produce identical cases"


def test_different_seeds_differ():
    import random
    a = router_benchmark.build_cases(random.Random(0), 100)
    b = router_benchmark.build_cases(random.Random(1), 100)
    assert a != b
