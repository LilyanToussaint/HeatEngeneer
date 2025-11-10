"""Registry of available heat-transfer coefficient correlations."""
from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Callable, Dict, Tuple

CorrelationCallable = Callable[..., float]


def _registry_key(name: str, func: CorrelationCallable) -> str:
    """Return the canonical registry key for a correlation function."""

    override = getattr(func, "correlation_name", None)
    if isinstance(override, str) and override:
        return override
    if name.startswith("h_"):
        return name[2:]
    return name


def _module_name_from_path(package_root: Path, module_path: Path) -> str:
    """Convert a module path to its importable dotted name."""

    relative = module_path.relative_to(package_root)
    parts = relative.with_suffix("").parts
    return ".".join((__name__, *parts))


def _discover_correlations() -> Tuple[Dict[str, CorrelationCallable], Dict[str, CorrelationCallable]]:
    """Import correlation modules dynamically and build the registry."""

    package_path = Path(__file__).resolve().parent
    registry: Dict[str, CorrelationCallable] = {}
    exports: Dict[str, CorrelationCallable] = {}

    for module_path in sorted(package_path.rglob("*.py")):
        if module_path.name == "__init__.py" or "__pycache__" in module_path.parts:
            continue

        module_name = _module_name_from_path(package_path, module_path)
        module = import_module(module_name)
        exported_names = getattr(module, "__all__", ())

        for attr_name in exported_names:
            attr = getattr(module, attr_name)
            if callable(attr) and getattr(attr, "metadata", None) is not None:
                key = _registry_key(attr_name, attr)
                registry[key] = attr
            exports[attr_name] = attr

    return registry, exports


HTC_CORRELATIONS, _EXPORTED_FUNCS = _discover_correlations()
globals().update(_EXPORTED_FUNCS)

__all__ = ["HTC_CORRELATIONS", *sorted(_EXPORTED_FUNCS)]
