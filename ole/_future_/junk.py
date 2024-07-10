import numpy as np
from specio.spectrometers import colorimetry_research

from ole.tpg_controller import TPGController

TPG_IP = "10.10.3.84"

tpg = TPGController(TPG_IP)
tpg.send_color((502, 502, 578))

meter = colorimetry_research.CRSpectrometer.discover()
meter.measurement_speed = colorimetry_research.MeasurementSpeed.FAST

ms = []
for _ in range(3):
    ms += [m := meter.measure()]
    print(m)

print(np.sum([m.exposure for m in ms]))
