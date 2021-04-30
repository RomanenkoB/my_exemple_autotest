import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel
import random

machineId = "6"

retailerId = ""

itemId = "38"

machinesAll = '''query {
  machinesAll{
    id, name, type, address1, address2, city, status, howToFind, longitude, zip,
  }
}'''

machine = '''query {
  machine(id: "%s"){
    id,name,type,status,address1,address2,city,status,location{id, timeOffset}
  }
}'''

machineItems = '''query{
  machineItems(filters:{machineId: "%s", retailerId: 1, isMachine: false} , first: 15){
    paginatorInfo{count,hasMorePages, currentPage, firstItem, lastPage,perPage, total}
    data{id, item{id, name}, quantity, availableQuantity, machine{id, type, workingHours, status, imageUrls{photo1}}},
  }
}'''

machineItem = '''query{
  machineItem(machineId: "%s", itemId: "%s"){
    id, quantity, availableQuantity, recPrice, medPrice, item{id, name}, machine{id, name}
  }
}'''

machines = '''query{
  machines(first: 10){
    paginatorInfo{count, firstItem, total},
    data{id, name, type, city, status}
  }
}'''


def test_machinesAll():
    global machineId
    start_time = time.time()
    r = requests.post(url, json={'query': machinesAll})
    try:
        assert r.json()["data"]["machinesAll"]
        machineId = random.randint(2, len((r.json()["data"]["machinesAll"])))
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", machinesAll)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], machinesAll)
        assert False


def test_machines():
    start_time = time.time()
    r = requests.post(url, json={'query': machines})
    try:
        assert r.json()["data"]["machines"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", machines)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], machines)
        assert False


def test_machine():
    start_time = time.time()
    r = requests.post(url, json={'query': machine % machineId})
    try:
        assert r.json()["data"]["machine"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", machine % machineId)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], machine % machineId)
        assert False


def test_machineItems():
    global itemId, machineId
    start_time = time.time()
    r = requests.post(url, json={'query': machineItems % machineId})
    try:
        assert r.json()["data"]["machineItems"]
        itemId = r.json()["data"]["machineItems"]["data"][0]['item']["id"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", machineItems % machineId)
        machineId = r.json()["data"]["machineItems"]["data"][0]['machine']["id"]
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], machineItems % machineId)
        assert False


def test_machineItem():
    start_time = time.time()
    r = requests.post(url, json={'query': machineItem % (machineId, itemId)})
    try:
        assert r.json()["data"]["machineItem"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", machineItem % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], machineItem % (machineId, itemId))
        assert False
