"""Registry of available heat-transfer coefficient correlations."""

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
from .dittus_boelter_internal import h_dittus_boelter_internal
from .eta_fin_annular import eta_fin_annular
from .eta_fin_rectangular import eta_fin_rectangular
from .flatplate_laminar import h_flatplate_laminar
from .flatplate_turbulent import h_flatplate_turbulent
from .gnielinski_internal import h_gnielinski_internal
from .gungor_winterton_flow_boiling import h_gungor_winterton_flow_boiling
from .hausen_laminar_developing import h_hausen_laminar_developing
from .hilpert_cylinder_crossflow import h_hilpert_cylinder_crossflow
from .kays_london_staggered_fin import h_kays_london_staggered_fin
from .manglik_bergles_offset_strip_fin import h_manglik_bergles_offset_strip_fin
from .nusselt_film_horizontal_tube import h_nusselt_film_horizontal_tube
from .nusselt_film_vertical_plate import h_nusselt_film_vertical_plate
from .packed_bed_wakao import h_packed_bed_wakao
from .petukhov_internal import h_petukhov_internal
from .rohsenow_pool_boiling import h_rohsenow_pool_boiling
from .shell_side_kern import h_shell_side_kern
from .shah_condensation_inside_tube import h_shah_condensation_inside_tube
from .shah_flow_boiling import h_shah_flow_boiling
from .shah_london_laminar_developing import h_shah_london_laminar_developing
from .sieder_tate_internal import h_sieder_tate_internal
from .whitaker_sphere import h_whitaker_sphere
from .zukauskas_tube_bank import h_zukauskas_tube_bank
from .h_effective_finned_surface import h_effective_finned_surface

HTC_CORRELATIONS = {
    "chen_flow_boiling": h_chen_flow_boiling,
    "churchill_bernstein_cylinder_crossflow": h_churchill_bernstein_cylinder_crossflow,
    "churchill_chu_horizontal_cylinder": h_churchill_chu_horizontal_cylinder,
    "churchill_chu_horizontal_plate_hot_down_cold_up": h_churchill_chu_horizontal_plate_hot_down_cold_up,
    "churchill_chu_horizontal_plate_hot_up_cold_down": h_churchill_chu_horizontal_plate_hot_up_cold_down,
    "churchill_chu_vertical_plate": h_churchill_chu_vertical_plate,
    "dittus_boelter_internal": h_dittus_boelter_internal,
    "eta_fin_annular": eta_fin_annular,
    "eta_fin_rectangular": eta_fin_rectangular,
    "flatplate_laminar": h_flatplate_laminar,
    "flatplate_turbulent": h_flatplate_turbulent,
    "gnielinski_internal": h_gnielinski_internal,
    "gungor_winterton_flow_boiling": h_gungor_winterton_flow_boiling,
    "hausen_laminar_developing": h_hausen_laminar_developing,
    "hilpert_cylinder_crossflow": h_hilpert_cylinder_crossflow,
    "h_effective_finned_surface": h_effective_finned_surface,
    "kays_london_staggered_fin": h_kays_london_staggered_fin,
    "manglik_bergles_offset_strip_fin": h_manglik_bergles_offset_strip_fin,
    "nusselt_film_horizontal_tube": h_nusselt_film_horizontal_tube,
    "nusselt_film_vertical_plate": h_nusselt_film_vertical_plate,
    "packed_bed_wakao": h_packed_bed_wakao,
    "petukhov_internal": h_petukhov_internal,
    "rohsenow_pool_boiling": h_rohsenow_pool_boiling,
    "shell_side_kern": h_shell_side_kern,
    "shah_condensation_inside_tube": h_shah_condensation_inside_tube,
    "shah_flow_boiling": h_shah_flow_boiling,
    "shah_london_laminar_developing": h_shah_london_laminar_developing,
    "sieder_tate_internal": h_sieder_tate_internal,
    "whitaker_sphere": h_whitaker_sphere,
    "zukauskas_tube_bank": h_zukauskas_tube_bank,
}

__all__ = ["HTC_CORRELATIONS"]
