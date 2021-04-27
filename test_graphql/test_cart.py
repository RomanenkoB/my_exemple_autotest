import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel
from pprint import pprint
from test_machine import machineId, itemId

carts = '''query{
  carts{
    machine{id, name,type, city, workingHours, status, imageUrls{photo1}},
    items{id, quantity, item{id, name, category, type, feelings, imageUrls{photo1}}},
    totalItems
  }
}'''


cart = '''query{
  cart(machineId: "%s"){
    machine{id, name,type, city, workingHours, status, imageUrls{photo1}},
    items{id, quantity, item{id, name, category, type, feelings, imageUrls{photo1}}}
    totalItems
  }
}'''

upsertCartItem = '''mutation {
  upsertCartItem(input: {machineId: "%s", itemId: "%s", quantity: 5}){
    id,
    quantity,
    item{id, name, category, type, feelings, imageUrls{photo1}, status},
    machineItem{id, quantity, availableQuantity, machine{id, type, workingHours, status, imageUrls{photo1}}},
  	favoriteItem{item{id, name, category, type, feelings, status, imageUrls{photo1}}}
  }
}'''

removeCartItem = '''mutation{
  removeCartItem(input: {machineId: "%s", itemId: "%s"})
}'''

emptyCart = '''mutation{
  emptyCart(input: {machineId: "%s"})
}'''


def test_upsertCartItem():
    start_time = time.time()
    r = requests.post(url, json={'query': upsertCartItem % (machineId, itemId)}, headers=headers)
    try:
        assert r.json()["data"]["upsertCartItem"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", upsertCartItem % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", upsertCartItem % (machineId, itemId))
        assert False


def test_carts():
    start_time = time.time()
    r = requests.post(url, json={'query': carts}, headers=headers)
    try:
        assert r.json()["data"]["carts"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", carts)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", carts)
        assert False


def test_cart():
    start_time = time.time()
    r = requests.post(url, json={'query': cart % machineId}, headers=headers)
    try:
        assert r.json()["data"]["cart"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", cart % machineId)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", cart % machineId)
        assert False


def test_removeCartItem():
    start_time = time.time()
    r = requests.post(url, json={'query': removeCartItem % (machineId, itemId)}, headers=headers)
    try:
        assert r.json()["data"]["removeCartItem"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", removeCartItem % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", removeCartItem % (machineId, itemId))
        assert False


def test_emptyCart():
    start_time = time.time()
    requests.post(url, json={'query': upsertCartItem % (machineId, itemId)}, headers=headers)
    r = requests.post(url, json={'query': emptyCart % machineId}, headers=headers)
    try:
        assert r.json()["data"]["emptyCart"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", emptyCart % machineId)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL", emptyCart % machineId)
        assert False

