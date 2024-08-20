# %% Load Imports
from pathlib import Path

import numpy as np
from colour.models.rgb.transfer_functions import st_2084
from matplotlib import pyplot as plt
from specio.serialization.csmf import (
    CSMF_Data,
    CSMF_Metadata,
    load_csmf_file,
    save_csmf_file,
)
from specio.spectrometers import colorimetry_research
from specio.spectrometers.common import VirtualSpectrometer

from ole._future_ import config as test_configs
from ole.ETC.analysis import ColourPrecisionAnalysis
from ole.ETC.pdf import generate_report_page
from ole.measurement_controllers import DisplayMeasureController, ProgressPrinter
from ole.test_colors import PQ_TestColorsConfig
from ole.tpg_controller import TPGController

# %% Consts

TPG_IP = "10.19.12.10"
TILE_STRING = "BP2v2 MVR, PQ, Native, DLUT Off"
SAVE_DIR = Path.home().joinpath("Downloads/proc_compare").expanduser()
SAVE_FILE = "bp2v2_mvr_native_02.csmf"

save_path = Path(SAVE_DIR).joinpath(SAVE_FILE).expanduser()
save_path = save_path.with_suffix(".csmf")
save_path.parent.mkdir(parents=True, exist_ok=True)

# config = test_configs.PQ_NATIVE_TEST
config = test_configs.ProcessorTestConfig(
    USE_VIRTUAL=False,
    TCC=PQ_TestColorsConfig(
        ramp_samples=31,
        ramp_repeats=1,
        mesh_size=13,
        blacks=10,
        whites=3,
        random=0,
        quantized_bits=10,
        first_light=0.025,
        max_nits=1450,  # Change based on tile data
    ),
    STABILIZATION_SECONDS=1.5,
    WARMUP_MINUTES=20,
    EOTF=st_2084.eotf_ST2084,
    EOTF_INV=st_2084.eotf_inverse_ST2084,
    NPM=None,
)
# %% Make Measurements

tpg = TPGController(TPG_IP)
tpg.send_color((800, 400, 800))

# %%

if config.USE_VIRTUAL:
    meter = VirtualSpectrometer()
else:
    meter = colorimetry_research.CRSpectrometer.discover()
    # meter.measurement_speed = colorimetry_research.MeasurementSpeed.NORMAL


dmc = DisplayMeasureController(
    tpg=tpg,
    cr=meter,
    color_list=config.TEST_COLORS,
    progress_callbacks=[ProgressPrinter()],
)
dmc.random_colors_duration = config.STABILIZATION_SECONDS

measurements = dmc.run_measurements(warmup_time=config.WARMUP_MINUTES * 60)
measurements = np.asarray(measurements)

tpg.send_color((0, 0, 0))

ml = CSMF_Data(
    measurements=measurements,
    order=config.TEST_COLORS.order,
    test_colors=config.TEST_COLORS.colors,
    metadata=CSMF_Metadata(notes=TILE_STRING),
)
save_csmf_file(str(save_path.resolve()), ml)

print(f"File Saved to: {save_path!s:s}")

# %% Analyze

data_path = Path(save_path)

# Uncoment to use native primaries from measurement file
data = load_csmf_file(data_path)

cpa = ColourPrecisionAnalysis(
    data,
    eotf=config.EOTF,
    eotf_inv=config.EOTF_INV,
    primary_matrix=config.NPM,
)

print(cpa)
# %% Generate PDF

fig = generate_report_page(cpa)

out_file_name = data_path.with_suffix(".pdf")
fig.savefig(str(out_file_name), facecolor=[1, 1, 1])

print(f"Analysis saved to: {out_file_name!s}")  # noqa: T201
plt.close(fig)

# %%
