"""Example usage of the Gnielinski internal heat-transfer correlation."""
from __future__ import annotations

from Source import HeatTransferCoefficient


def compute_example() -> None:
    """Compute and print the heat-transfer coefficient using Gnielinski."""
    htc = HeatTransferCoefficient("gnielinski_internal")
    result = htc.compute(Re=2.5e4, Pr=7.0, k=0.6, d_i=0.01)

    print("=== Gnielinski internal correlation ===")
    print(f"Heat-transfer coefficient: {result.h:.2f} W/(m^2·K)")
    print(f"Correlation valid: {result.valid} ({result.message})")
    print("Metadata:")
    for key, value in sorted(result.correlation_meta.items()):
        print(f"  - {key}: {value}")


if __name__ == "__main__":
    compute_example()
