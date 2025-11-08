"""Helper script to execute the project's unit tests."""
from __future__ import annotations

from pathlib import Path
import unittest


def run_tests() -> unittest.result.TestResult:
    """Discover and run all unit tests from the ``Test`` package."""
    repo_root = Path(__file__).resolve().parent.parent
    test_dir = repo_root / "Test"
    loader = unittest.TestLoader()
    suite = loader.discover(str(test_dir))
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_tests()
