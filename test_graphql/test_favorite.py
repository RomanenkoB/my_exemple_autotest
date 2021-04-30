import requests
import time
from env import url, mass_reports, headers
import traceback
from helpers import report_csv, report_exel
from test_machine import machineId, itemId


favoriteItems = '''query{
    favoriteItems(filters: {retailerId: 2, machineId: "%s"},first: 10){
    data {item{id, name, category, type, status, feelings, imageUrls{photo1}}, 
      machineItem{id, quantity, availableQuantity, isFavoriteItem, quantityInCart, machine{id, type, workingHours,
       status, imageUrls{photo1}}}},
    }
}'''

upsertFavoriteItem = '''mutation{
  upsertFavoriteItem(input: {machineId: "%s", itemId: "%s"})
}'''

removeFavoriteItem = '''mutation{
  removeFavoriteItem(input: {machineId: "%s", itemId: "%s"})
}'''


def test_upsertFavoriteItem():
    start_time = time.time()
    r = requests.post(url, json={'query': upsertFavoriteItem % (machineId, itemId)}, headers=headers)
    try:
        assert r.json()["data"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", upsertFavoriteItem % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], upsertFavoriteItem % (machineId, itemId))
        assert False


def test_favorite():
    start_time = time.time()
    r = requests.post(url, json={'query': favoriteItems % machineId}, headers=headers)
    try:
        assert r.json()["data"]["favoriteItems"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", favoriteItems)
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], favoriteItems)
        assert False


def test_removeFavoriteItem():
    start_time = time.time()
    r = requests.post(url, json={'query': removeFavoriteItem % (machineId, itemId)}, headers=headers)
    try:
        assert r.json()["data"]["removeFavoriteItem"]
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "SUCCESSFUL", removeFavoriteItem % (machineId, itemId))
    except:
        report_exel(r, start_time, traceback.extract_stack()[-1][2], "FAIL - " + r.json()["errors"][0]["extensions"]["category"] + "\n" + r.json()["errors"][0]["message"], removeFavoriteItem % (machineId, itemId))
        assert False