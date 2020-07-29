from Data.PreProcessing import convertToCSV
from Data.PreProcessing import fetchData
from Data.PreProcessing import fetchLabels
from Algorithms.testingUtil import getScore
from Algorithms.testingUtil import plotTracing

fileName = "mar9-data5-PLX-DAQ.xlsx"
csvFileName = convertToCSV(fileName)
data = fetchData(csvFileName)

year = int(2020)
month = int(3)
day = int(9)
latitude = int(48.463522)
longitude = int(-123.310644)
timezone = int(-8)
Labels = fetchLabels(data, year, month, day, latitude, longitude, timezone)

getScore(Labels,Labels,5)
plotTracing(None,None,Labels)