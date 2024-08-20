from dataclasses import dataclass
from typing import Callable

from colour.colorimetry.datasets.illuminants.chromaticity_coordinates import (
    CCS_ILLUMINANTS_CIE_STANDARD_OBSERVER_2_DEGREE_CIE1931,
)
from colour.hints import ArrayLike
from colour.models.rgb.datasets import dci_p3, itur_bt_2020
from colour.models.rgb.derivation import normalised_primary_matrix
from colour.models.rgb.transfer_functions import st_2084
from colour.models.rgb.transfer_functions.gamma import gamma_function

from ole.test_colors import PQ_TestColorsConfig, TestColorsConfig, generate_colors

MAX_NITS = 1450


def GAMMA24_EOTF(x):
    return (
        gamma_function(x, exponent=2.4, negative_number_handling="preserve") * MAX_NITS
    )


def GAMMA24_EOTF_INVERSE(x):
    return gamma_function(
        x / MAX_NITS, exponent=1 / 2.4, negative_number_handling="preserve"
    )


DEFAULT_P3_NPM = normalised_primary_matrix(
    dci_p3.PRIMARIES_DCI_P3,
    CCS_ILLUMINANTS_CIE_STANDARD_OBSERVER_2_DEGREE_CIE1931["D65"],
)

DEFAULT_2020_NPM = normalised_primary_matrix(
    itur_bt_2020.PRIMARIES_BT2020,
    CCS_ILLUMINANTS_CIE_STANDARD_OBSERVER_2_DEGREE_CIE1931["D65"],
)


@dataclass
class ProcessorTestConfig:
    USE_VIRTUAL: bool
    TCC: PQ_TestColorsConfig | TestColorsConfig
    STABILIZATION_SECONDS: float
    WARMUP_MINUTES: float
    EOTF: Callable
    EOTF_INV: Callable
    NPM: ArrayLike | None

    def __post_init__(self):
        self.TEST_COLORS = generate_colors(self.TCC)


FAST_PQ_NATIVE_TEST = ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=PQ_TestColorsConfig(
        ramp_samples=7,
        ramp_repeats=1,
        mesh_size=2,
        blacks=5,
        whites=5,
        random=0,
        quantized_bits=10,
        first_light=0.2,
        max_nits=1450,  # Change based on tile data
    ),
    STABILIZATION_SECONDS=0,
    WARMUP_MINUTES=0,
    EOTF=st_2084.eotf_ST2084,
    EOTF_INV=st_2084.eotf_inverse_ST2084,
    NPM=None,
)

PQ_NATIVE_TEST = ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=PQ_TestColorsConfig(
        ramp_samples=29,
        ramp_repeats=1,
        mesh_size=15,
        blacks=10,
        whites=3,
        random=0,
        quantized_bits=10,
        first_light=0.025,
        max_nits=1400,  # Change based on tile data
    ),
    STABILIZATION_SECONDS=0.25,
    WARMUP_MINUTES=10,
    EOTF=st_2084.eotf_ST2084,
    EOTF_INV=st_2084.eotf_inverse_ST2084,
    NPM=None,
)

P3_GAMMA24_TEST = ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=TestColorsConfig(
        ramp_samples=25,
        ramp_repeats=1,
        mesh_size=7,
        blacks=15,
        whites=3,
        random=0,
        quantized_bits=10,
    ),
    STABILIZATION_SECONDS=3,
    WARMUP_MINUTES=10,
    EOTF=GAMMA24_EOTF,
    EOTF_INV=GAMMA24_EOTF,
    NPM=DEFAULT_P3_NPM,
)

FAST_P3_GAMMA24_TEST = ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=TestColorsConfig(
        ramp_samples=5,
        ramp_repeats=1,
        mesh_size=2,
        blacks=3,
        whites=2,
        random=0,
        quantized_bits=10,
    ),
    STABILIZATION_SECONDS=0,
    WARMUP_MINUTES=0,
    EOTF=GAMMA24_EOTF,
    EOTF_INV=GAMMA24_EOTF,
    NPM=DEFAULT_P3_NPM,
)

R2020_PQ_TEST = ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=PQ_TestColorsConfig(
        ramp_samples=31,
        ramp_repeats=1,
        mesh_size=7,
        blacks=15,
        whites=3,
        random=0,
        quantized_bits=10,
        first_light=0.05,
        max_nits=1400,
    ),
    STABILIZATION_SECONDS=0,
    WARMUP_MINUTES=0,
    EOTF=st_2084.eotf_ST2084,
    EOTF_INV=st_2084.eotf_inverse_ST2084,
    NPM=DEFAULT_2020_NPM,
)
