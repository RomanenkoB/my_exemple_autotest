import pytest
from helpers import registration


def test_registration(initial_wd):
    wd = initial_wd
    try:
        registration(wd)
        assert True
    except:
        wd.quit()
        assert False

