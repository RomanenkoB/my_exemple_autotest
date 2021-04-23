import pytest
from selenium import webdriver


@pytest.fixture()
def initial_wd():
    """Инициализация веб-драйвера"""
    wd = webdriver.Chrome()
    wd.maximize_window()
    wd.implicitly_wait(20)
    return wd


