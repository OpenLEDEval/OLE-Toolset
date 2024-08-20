from time import perf_counter

from specio.spectrometers import colorimetry_research

meter = colorimetry_research.CRSpectrometer.discover()
meter.measurement_speed = colorimetry_research.MeasurementSpeed.NORMAL

t1 = perf_counter()
m = meter.measure()
t2 = perf_counter()
print(t2 - t1)
print(m)
