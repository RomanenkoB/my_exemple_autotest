import pytest
from helpers import login


def test_login(initial_wd):
    wd = initial_wd
    try:
        result = login(wd)
        assert result
    except:
        wd.quit()
        assert False