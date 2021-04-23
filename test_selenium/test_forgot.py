import pytest
from helpers import forgot


def test_forgot(initial_wd):
    wd = initial_wd
    try:
        result = forgot(wd)
        assert result
    except:
        wd.quit()
        assert False