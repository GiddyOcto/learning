import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
import consts

sa = gspread.service_account(filename=consts.creds)

def insertRow(listOfItems):
    sh = sa.open("Spends")
    wks = sh.worksheet("telegram")

    wks.insert_row(listOfItems, 2)

def getRunningTotal(currentMonth):
    sh = sa.open("Spends")
    wks = sh.worksheet("telegram")

    runningTotal = 0

    max = wks.row_count
    maxCell = ("C"+str(max))
    allSpends = wks.get('A2:'+maxCell)

    for spend in allSpends:
        month = (str(spend[2])[5:7])
        amountSpent = int(spend[1])
        if int(month) == currentMonth:
            runningTotal = runningTotal + amountSpent
    return str(runningTotal)
