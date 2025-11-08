"""Registry of available heat-transfer coefficient correlations."""

from .gnielinski_internal import h_gnielinski_internal
from .dittus_boelter_internal import h_dittus_boelter_internal

HTC_CORRELATIONS = {
    "gnielinski_internal": h_gnielinski_internal,
    "dittus_boelter_internal": h_dittus_boelter_internal,
}

__all__ = ["HTC_CORRELATIONS"]
