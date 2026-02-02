from unittest import TestCase

from MainDeviceScripts.Algorithm_support.getOutBytesDef import get_out_bytes_to_PLC_from_SMBlock


class Test(TestCase):
    def test_get_out_bytes_to_plc_from_smblock(self):
        val = ["X0_2", 0, "X0_4", "0", "X1_2"]
        assert get_out_bytes_to_PLC_from_SMBlock(val)
