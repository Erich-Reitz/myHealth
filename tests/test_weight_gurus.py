# standard library
from unittest.mock import patch

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

    @patch("health.weight_gurus.WeightGurus._do_login")
    @patch("health.weight_gurus.WeightGurus._get_weight_history")
    def test_get_all(self, mock_do_login, mock_get_weight_history, weight_guru ):
        mock_get_weight_history.return_value = {"Operations": ""}
        weight_guru.get_all()
        
        mock_do_login.assert_called_once()

    def test_wg_num_to_float_pass(self, weight_guru):
        assert weight_guru._wg_num_to_float("2141") == 214.1

    def test_wg_num_to_float_raises(self, weight_guru):
        with pytest.raises(exceptions.UnknownBehavior):
            weight_guru._wg_num_to_float("1") 
