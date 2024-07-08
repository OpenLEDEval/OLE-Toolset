# %% Load Imports
from pathlib import Path

import numpy as np
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
from ole.tpg_controller import TPGController

# %% Consts

TPG_IP = "10.10.3.84"
TILE_STRING = "DS MPLED 2020 PQ"
SAVE_DIR = Path.home().joinpath("Downloads").expanduser()
SAVE_FILE = "ds_pq_2020.csmf"

# %% Make Measurements

config = test_configs.PQ_NATIVE_TEST

tpg = TPGController(TPG_IP)
tpg.send_color((800, 400, 800))

# %%

if config.USE_VIRTUAL:
    meter = VirtualSpectrometer()
else:
    meter = colorimetry_research.CRSpectrometer.discover()
    meter.measurement_speed = colorimetry_research.MeasurementSpeed.FAST


dmc = DisplayMeasureController(
    tpg=tpg,
    cr=meter,
    color_list=config.TEST_COLORS,
    progress_callbacks=[ProgressPrinter()],
)
dmc.random_colors_duration = config.STABILIZATION_SECONDS

save_path = Path(SAVE_DIR).joinpath(SAVE_FILE).expanduser()
save_path = save_path.with_suffix(".csmf")
save_path.parent.mkdir(parents=True, exist_ok=True)

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
