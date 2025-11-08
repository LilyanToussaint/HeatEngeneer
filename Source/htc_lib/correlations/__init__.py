"""Registry of available heat-transfer coefficient correlations."""
from __future__ import annotations

from .array_jet_impingement import h_array_jet_impingement
from .chen_flow_boiling import h_chen_flow_boiling
from .churchill_bernstein_cylinder_crossflow import (
    h_churchill_bernstein_cylinder_crossflow,
)
from .churchill_chu_horizontal_cylinder import h_churchill_chu_horizontal_cylinder
from .churchill_chu_horizontal_plate_hot_down_cold_up import (
    h_churchill_chu_horizontal_plate_hot_down_cold_up,
)
from .churchill_chu_horizontal_plate_hot_up_cold_down import (
    h_churchill_chu_horizontal_plate_hot_up_cold_down,
)
from .churchill_chu_vertical_plate import h_churchill_chu_vertical_plate
from .circular_jet_impingement_singlephase import (
    h_circular_jet_impingement_singlephase,
)
from .dittus_boelter_internal import h_dittus_boelter_internal
from .eta_fin_annular import eta_fin_annular
from .eta_fin_rectangular import eta_fin_rectangular
from .fanning_f_to_dp import fanning_f_to_dp
from .finned_tube_bank_eta_global import h_finned_tube_bank_eta_global
from .flatplate_laminar import h_flatplate_laminar
from .flatplate_turbulent import h_flatplate_turbulent
from .gnielinski_internal import h_gnielinski_internal
from .gungor_winterton_flow_boiling import h_gungor_winterton_flow_boiling
from .h_effective_finned_surface import h_effective_finned_surface
from .hausen_laminar_developing import h_hausen_laminar_developing
from .hilpert_cylinder_crossflow import h_hilpert_cylinder_crossflow
from .high_pressure_gas import h_high_pressure_gas
from .j_colburn_to_h import j_colburn_to_h
from .kandlikar_microchannel_boiling import h_kandlikar_microchannel_boiling
from .kandlikar_singlephase_microchannel import h_kandlikar_singlephase_microchannel
from .kays_london_staggered_fin import h_kays_london_staggered_fin
from .liquid_metal_internals import h_liquid_metal_internals
from .louvered_fin_kays_london import h_louvered_fin_kays_london
from .low_pr_forced_convection import h_low_Pr_forced_convection
from .manglik_bergles_offset_strip_fin import h_manglik_bergles_offset_strip_fin
from .microchannel_laminar_developing import h_microchannel_laminar_developing
from .nusselt_film_horizontal_tube import h_nusselt_film_horizontal_tube
from .nusselt_film_vertical_plate import h_nusselt_film_vertical_plate
from .offset_strip_fin_manglik_bergles import h_offset_strip_fin_manglik_bergles
from .packed_bed_wakao import h_packed_bed_wakao
from .petukhov_internal import h_petukhov_internal
from .rohsenow_pool_boiling import h_rohsenow_pool_boiling
from .shell_side_kern import h_shell_side_kern
from .shah_condensation_inside_tube import h_shah_condensation_inside_tube
from .shah_flow_boiling import h_shah_flow_boiling
from .shah_london_laminar_developing import h_shah_london_laminar_developing
from .sieder_tate_internal import h_sieder_tate_internal
from .wavy_fin_correlation import h_wavy_fin_correlation
from .whitaker_sphere import h_whitaker_sphere
from .zukauskas_inline_tube_bank import h_zukauskas_inline_tube_bank
from .zukauskas_staggered_tube_bank import h_zukauskas_staggered_tube_bank
from .zukauskas_tube_bank import h_zukauskas_tube_bank

HTC_CORRELATIONS = {
    "array_jet_impingement": h_array_jet_impingement,
    "chen_flow_boiling": h_chen_flow_boiling,
    "churchill_bernstein_cylinder_crossflow": h_churchill_bernstein_cylinder_crossflow,
    "churchill_chu_horizontal_cylinder": h_churchill_chu_horizontal_cylinder,
    "churchill_chu_horizontal_plate_hot_down_cold_up": h_churchill_chu_horizontal_plate_hot_down_cold_up,
    "churchill_chu_horizontal_plate_hot_up_cold_down": h_churchill_chu_horizontal_plate_hot_up_cold_down,
    "churchill_chu_vertical_plate": h_churchill_chu_vertical_plate,
    "circular_jet_impingement_singlephase": h_circular_jet_impingement_singlephase,
    "dittus_boelter_internal": h_dittus_boelter_internal,
    "eta_fin_annular": eta_fin_annular,
    "eta_fin_rectangular": eta_fin_rectangular,
    "finned_tube_bank_eta_global": h_finned_tube_bank_eta_global,
    "flatplate_laminar": h_flatplate_laminar,
    "flatplate_turbulent": h_flatplate_turbulent,
    "gnielinski_internal": h_gnielinski_internal,
    "gungor_winterton_flow_boiling": h_gungor_winterton_flow_boiling,
    "h_effective_finned_surface": h_effective_finned_surface,
    "hausen_laminar_developing": h_hausen_laminar_developing,
    "hilpert_cylinder_crossflow": h_hilpert_cylinder_crossflow,
    "high_pressure_gas": h_high_pressure_gas,
    "j_colburn_to_h": j_colburn_to_h,
    "kandlikar_microchannel_boiling": h_kandlikar_microchannel_boiling,
    "kandlikar_singlephase_microchannel": h_kandlikar_singlephase_microchannel,
    "kays_london_staggered_fin": h_kays_london_staggered_fin,
    "liquid_metal_internals": h_liquid_metal_internals,
    "louvered_fin_kays_london": h_louvered_fin_kays_london,
    "low_Pr_forced_convection": h_low_Pr_forced_convection,
    "manglik_bergles_offset_strip_fin": h_manglik_bergles_offset_strip_fin,
    "microchannel_laminar_developing": h_microchannel_laminar_developing,
    "nusselt_film_horizontal_tube": h_nusselt_film_horizontal_tube,
    "nusselt_film_vertical_plate": h_nusselt_film_vertical_plate,
    "offset_strip_fin_manglik_bergles": h_offset_strip_fin_manglik_bergles,
    "packed_bed_wakao": h_packed_bed_wakao,
    "petukhov_internal": h_petukhov_internal,
    "rohsenow_pool_boiling": h_rohsenow_pool_boiling,
    "shell_side_kern": h_shell_side_kern,
    "shah_condensation_inside_tube": h_shah_condensation_inside_tube,
    "shah_flow_boiling": h_shah_flow_boiling,
    "shah_london_laminar_developing": h_shah_london_laminar_developing,
    "sieder_tate_internal": h_sieder_tate_internal,
    "wavy_fin_correlation": h_wavy_fin_correlation,
    "whitaker_sphere": h_whitaker_sphere,
    "zukauskas_inline_tube_bank": h_zukauskas_inline_tube_bank,
    "zukauskas_staggered_tube_bank": h_zukauskas_staggered_tube_bank,
    "zukauskas_tube_bank": h_zukauskas_tube_bank,
}

__all__ = ["HTC_CORRELATIONS", "fanning_f_to_dp"]
