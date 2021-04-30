import requests
import time
from env import url, mass_reports
import traceback
from helpers import report_exel, report_csv

brands_filter = '''query {
  brands(filters: {retailerId: "1", machineId: "1"}){
    id, 
    name
  }
}
'''

brands = '''query {
  brands{
    id, 
    name
  }
}'''


def test_brands():
    """Test dock"""
    start_time = time.time()
    r = requests.post(url, json={'query': brands})
    try:
        assert r.json()["data"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", brands)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], brands)
        assert False


def test_brands_filter():
    start_time = time.time()
    r = requests.post(url, json={'query': brands_filter})
    try:
        assert r.json()["data"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", brands_filter)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], brands_filter)
        assert False


