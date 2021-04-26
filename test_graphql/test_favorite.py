import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel


favoriteItems = '''query{
    favoriteItems(first: 1){
    data {id, item{id, name, category}, machines{id, name}},
    }
}'''


def test_favorite():
    start_time = time.time()
    r = requests.post(url, json={'query': favoriteItems}, headers=headers)
    try:
        assert r.json()["data"]["favoriteItems"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", favoriteItems)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", favoriteItems)
        assert False