from unittest import TestCase

from Modules.DI8 import digital_inputs


class Test(TestCase):
    def test_digital_inputs(self):
        val1, val2 = digital_inputs([1,1,1,1,1,1,1,1], True, False, False,)
        print(val1)
        print(val2)
        self.fail()
