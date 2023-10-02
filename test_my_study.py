import pytest
import requests
import json


def generateFutureDate(countDay):
    futureDate = (datetime.date.today() + relativedelta(days=(countDay))).strftime('%d.%m.%Y')
    return futureDate

def test_myfunction():
    mydata = generateFutureDate(100)
    print(mydata)