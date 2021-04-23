import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel
from pprint import pprint

machineId = "6"

itemId = "38"

preorderId = ""

saleOrders = '''query{
  saleOrders(first: 10){
    paginatorInfo{count, currentPage, firstItem, hasMorePages, lastItem, lastPage, perPage, total},
    data{id, createdAt, date, type, status, total, taxRates{id, name, value, recreational, medical}, machine{id, name, 
    type, workingHours, status, imageUrls{photo1}}},
  }
}'''


saleOrder = '''query{
  saleOrder(id: 1){
    id, createdAt, type, status, total, taxRates{id, name, value, recreational, medical}, 
        machine{id, name, type, workingHours, status, imageUrls{photo1}}, items{id, type, price, quantity, tax, quantity,
            item{id, name, category, type, feelings, imageUrls{photo1}}}
  }
}'''


createPreOrder = '''mutation{
  createPreOrder(input: {machineId: "%s", items: {id: "%s", quantity: 1}}){
    id, createdAt, total, machine{id, name}
  }
}'''

cancelPreOrder = '''mutation{
  cancelPreOrder(input: {id: "%s"}){
    id, createdAt, type, status, total, taxRates{id, name, value, recreational, medical}, machine{id, name, type, workingHours, 
    status, imageUrls{photo1}}, items{id, type, price, quantity, tax, quantity, item{id, name, category, type, feelings, 
    imageUrls{photo1}}}
  }
}'''


def test_saleOrders():
    start_time = time.time()
    r = requests.post(url, json={'query': saleOrders}, headers=headers)
    try:
        assert r.json()["data"]["saleOrders"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", saleOrders)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", saleOrders)
        assert False


def test_saleOrder():
    start_time = time.time()
    r = requests.post(url, json={'query': saleOrder}, headers=headers)
    try:
        assert r.json()["data"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", saleOrder)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", saleOrder)
        assert False


def test_createPreOrder():
    global preorderId
    start_time = time.time()
    r = requests.post(url, json={'query': createPreOrder % (machineId, itemId)}, headers=headers)
    try:
        assert r.json()["data"]["createPreOrder"]
        preorderId = r.json()["data"]["createPreOrder"]["id"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", createPreOrder % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", createPreOrder % (machineId, itemId))
        assert False


def test_cancelPreOrder():
    start_time = time.time()
    r = requests.post(url, json={'query': cancelPreOrder % preorderId}, headers=headers)
    try:
        assert r.json()["data"]["cancelPreOrder"]["status"] == "CANCELED"
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", cancelPreOrder % preorderId)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", cancelPreOrder % preorderId)
        assert False