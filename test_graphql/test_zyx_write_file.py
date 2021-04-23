from datetime import datetime
from env import mass_reports
from helpers import add_report_csv, add_report_exel

""" Тест-Файл для взыва функции создания конечного репорта.
    Вызов этого файла должен происходить в самую последнюю очередь, 
    поэтому он называется zyx (Последние буквы латинского алфавита), 
    При необходимости созания репорта не на все файлы теста, а лишь на некоторые
    можно сделать такую команду: pytest -s -v test_namefile.py::test_zyx_write_file.py 
"""

def test_add_report():
    assert add_report_exel()
    # assert add_report_csv()