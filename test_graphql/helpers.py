import requests
import time
from env import url, mass_reports, headers_exel, Name_test, Rout, Status, Assert_status, Time_response, Time_test, Body
from datetime import datetime
import pandas as pd


def report_csv(r, start_time, name_test, result, body=""):
    report_str = "{}|{}|{}|{}|{}|{}".format(name_test, r.url, r.status_code, result,
                                        r.elapsed.total_seconds(),
                                        time.time() - start_time)
    mass_reports.append(report_str)


def add_report_csv():
    try:
        now = datetime.strftime(datetime.now(), "%Y.%m.%d_%H:%M")
        header = "Name test|Rout|Status|Assert Status|Time response|Time test"
        with open("reports/report_" + now + ".csv", "a") as f:
            f.writelines(header + "\n")
            for item in mass_reports:
                f.writelines(item + "\n")
        return True
    except:
        return False


def report_exel(r, start_time, name_test, result, body):
    Name_test.append(name_test)
    Rout.append(r.url)
    Status.append(r.status_code)
    Assert_status.append(result)
    Time_response.append(r.elapsed.total_seconds())
    Time_test.append(time.time() - start_time)
    Body.append(body)


def add_report_exel():
    df = pd.DataFrame({
        headers_exel[0]: Name_test,
        headers_exel[1]: Rout,
        headers_exel[2]: Status,
        headers_exel[3]: Assert_status,
        headers_exel[4]: Time_response,
        headers_exel[5]: Time_test,
        headers_exel[6]: Body,
    })
    now = datetime.strftime(datetime.now(), "%Y.%m.%d_%H:%M")
    writer = pd.ExcelWriter("test_graphql/reports/report_" + now + ".xlsx", engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='report')
    setting_worksheet(writer)
    return True


def setting_worksheet(writer):
    worksheet = writer.sheets['report']
    worksheet.set_zoom(90)
    worksheet.set_column('A:A', 14)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('D:D', 30)
    worksheet.set_column('E:F', 16)
    worksheet.set_column('G:G', 40)
    for i in range(1, len(Name_test) + 1):
        worksheet.set_row(i, 90)
    writer.save()
