import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel
from pprint import pprint

retailer_domain = "Friesen, Schamberger and Hilpert@domain.com"

retailer_id = "1"

retailers = '''query{
  retailers(first: 10){
    paginatorInfo{count, firstItem, total},
    data{id, name, domain, primaryPhone, primaryEmail, city, address1}
  }
}'''


retailer = '''query {
  retailer(id: "%s"){
    id, name, domain, primaryPhone, primaryEmail, city, address1, address2, priceRangeInMachines
    }
  }'''


retailerByDomain = '''query{
  retailerByDomain(domain: "%s"){
     id, name, domain, primaryPhone, primaryEmail, city, address1, address2, priceRangeInMachines
  }
}'''


def test_retailers():
    global retailer_domain, retailer_id
    start_time = time.time()
    r = requests.post(url, json={'query': retailers})
    retailer_id = r.json()["data"]["retailers"]["data"][0]["id"]
    retailer_domain = r.json()["data"]["retailers"]["data"][0]["domain"]
    try:
        assert r.json()["data"]["retailers"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", retailers)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", retailers)
        assert False


def test_retailer():
    start_time = time.time()
    r = requests.post(url, json={'query': retailer % retailer_id})
    try:
        assert r.json()["data"]["retailer"]["id"] == retailer_id
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", retailer % retailer_id)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", retailer % retailer_id)
        assert False


def test_retailerByDomain():
    start_time = time.time()
    r = requests.post(url, json={'query': retailerByDomain % retailer_domain})
    try:
        assert r.json()["data"]["retailerByDomain"]["domain"] == retailer_domain
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", retailerByDomain % retailer_domain)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", retailerByDomain % retailer_domain)
        assert False


