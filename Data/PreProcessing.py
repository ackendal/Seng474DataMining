import pandas as pd
from pyephem_sunpath.sunpath import sunpos
from datetime import datetime
# import numpy as np
import csv


def convertToCSV(fileName):
    rawFile = fileName
    rawFilePath = 'Data/RawData/'+rawFile
    rawName = (rawFile.split("."))[0]
    csvName = "Data/csvData/" + rawName + '.csv'
    dataFrame = pd.read_excel(rawFilePath)
    dataFrame.to_csv(csvName, index = False, header=True)
    return csvName


def fetchData(fileName):
    results = []
    with open(fileName) as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)

    results.remove(results[0])
    for entry in results:
        time = entry[0]
        time = time.split(":")
        hour = time[0]
        minute = time[1]
        second = time[2]
        entry.remove(entry[0])
        entry.append(hour)
        entry.append(minute)
        entry.append(second)

    returnArray = []
    for entry in results:
        newEntry = []
        for value in entry:
            newEntry.append(float(value))
        returnArray.append(newEntry)
    return returnArray

def fetchLabels(data, year, month, day, latitude, longitude, timezone):
    Labels = []
    for entry in data:
        result = []
        hour = int(entry[6])
        minute = int(entry[7])
        second = int(data[0][8])
        result = fetchLabel(year, month, day, hour, minute, second, latitude, longitude, timezone)
        Labels.append(result)
    return Labels

def fetchLabel(year, month, date, hour, minute, second, latitude, longitude, timezone):
    returnLabels = []
    thetime = datetime(year, month, date, hour, minute, second)
    lat = latitude
    lon = longitude
    tz = timezone

    alt, azm = sunpos(thetime, lat, lon, tz, dst=False)
    returnLabels.append(alt)
    returnLabels.append(azm)
    return returnLabels