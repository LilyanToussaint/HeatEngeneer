"""Compatibility wrapper around the Manglik-Bergles offset-strip fin correlation."""
from __future__ import annotations

from .manglik_bergles_offset_strip_fin import h_manglik_bergles_offset_strip_fin


_METADATA = getattr(h_manglik_bergles_offset_strip_fin, "metadata", {
    "domain": "external",
    "convection": "forced",
    "geometry": "offset strip fin",
})


def h_offset_strip_fin_manglik_bergles(*args, **kwargs):
    """Delegate to :func:`h_manglik_bergles_offset_strip_fin` for backwards compatibility."""

    return h_manglik_bergles_offset_strip_fin(*args, **kwargs)


h_offset_strip_fin_manglik_bergles.metadata = _METADATA.copy()


__all__ = ["h_offset_strip_fin_manglik_bergles"]
