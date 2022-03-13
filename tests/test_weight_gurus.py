# standard library
import unittest

# third party
import pytest

# this package
from health import weight_gurus
from health import exceptions


@pytest.fixture
def weight_guru():
    return weight_gurus.WeightGurus("username", "password")



class TestWeightGuru():
    """Basic test cases."""
    def test_wg_num_to_float_pass(self, weight_guru):
        assert weight_guru._wg_num_to_float("2141") == 214.1

    def test_wg_num_to_float_raises(self, weight_guru):
        with pytest.raises(exceptions.UnknownBehavior):
            weight_guru._wg_num_to_float("1") 
