from pathlib import Path

import numpy as np
import pytest
from sklearn.covariance import EllipticEnvelope
from specio.serialization.csmf import load_csmf_file

from ole.ETC.analysis import ColourPrecisionAnalysis


class TestAnalysis:
    def test_cpa_pq_regresssion(self, monkeypatch):

        # Disable random start in primary matrix calculation, Useful when
        # detecting regressions with fewer false false positives. However, CPA
        # should be "deterministic" in that it should produce reliable values
        # without this patch.
        monkeypatch.setitem(
            EllipticEnvelope.__init__.__kwdefaults__, "random_state", 0x07FD
        )

        data_path = Path(__file__).parent.joinpath("data/e7618ddf.csmf")
        data = load_csmf_file(data_path)
        cpa = ColourPrecisionAnalysis(data)

        # fmt: off
        historical_pm = np.array(
            [[  6.07428777e-01,   1.79501928e-01,   1.62495763e-01],
             [  2.69323624e-01,   6.48831310e-01,   8.18450666e-02],
             [  7.65390155e-04,   5.42357721e-02,   1.00737465e+00]]
        )
        # fmt: on

        assert cpa.error["XYZ"].mean() == pytest.approx(
            32.732599948468568, abs=cpa.white["peak"][1] * 0.002
        )
        assert cpa.error["ICtCp"].mean() == pytest.approx(6.4747959074627239, rel=0.005)
        assert cpa.error["dI"].mean() == pytest.approx(4.8804443254176801, rel=0.005)
        assert cpa.error["dChromatic"].mean() == pytest.approx(
            3.6286910546792206, rel=0.005
        )
        assert cpa.error["dE2000"].mean() == pytest.approx(
            2.3667535510267408, rel=0.005
        )

        pass  # noqa: PIE790
