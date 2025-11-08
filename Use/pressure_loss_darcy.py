"""Example usage of the Darcy-Weisbach pressure-loss correlation."""
from __future__ import annotations

from pathlib import Path
import sys


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from Source import PressureLossCorrelation


def compute_example() -> None:
    """Compute and print the pressure drop for a straight circular duct."""
    correlation = PressureLossCorrelation("darcy_weisbach")
    result = correlation.compute(
        friction_factor=0.02,
        length=5.0,
        diameter=0.05,
        density=997.0,
        velocity=2.0,
    )

    print("=== Darcy-Weisbach pressure-loss correlation ===")
    print(f"Pressure drop: {result.delta_p:.2f} Pa")
    print(f"Correlation valid: {result.valid} ({result.message})")
    print("Metadata:")
    for key, value in sorted(result.correlation_meta.items()):
        print(f"  - {key}: {value}")


if __name__ == "__main__":
    compute_example()
