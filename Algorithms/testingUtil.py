import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import sin
from math import cos

def getScore(calculatedLabels, expectedLabels, degreeVariance):
    score = 0
    total = len(calculatedLabels)
    print("Tolerance of "+str(degreeVariance)+" degrees")
    for i in range (total):
        calculatedAlpha = calculatedLabels[i][0]
        calculatedBeta = calculatedLabels[i][1]
        expectedAlpha = expectedLabels[i][0]
        expectedBeta = expectedLabels[i][1]

        differenceBound = degreeVariance/2

        upperboundAlpha = expectedAlpha + differenceBound
        lowerboundAlpha = expectedAlpha - differenceBound
        upperboundBeta = expectedBeta + differenceBound
        lowerboundBeta = expectedBeta - differenceBound

        if (calculatedAlpha > upperboundAlpha) or (calculatedAlpha < lowerboundAlpha):
            continue
        elif (calculatedBeta > upperboundBeta) or (calculatedBeta < lowerboundBeta):
            continue

        score = score + 1
    print("Score: "+str(100 * score/total)+"%\n")
    return score/total

def processLabels(data):
    returnData = []
    elevation = 0
    azimuth = 1
    r = 1
    for entry in data:
        newEntry = []

        x = r * cos(entry[elevation]) * cos(entry[azimuth])
        y = r * cos(entry[elevation]) * sin(entry[azimuth])
        z = r * sin(entry[elevation])
        
        newEntry.append(x)
        newEntry.append(y)
        newEntry.append(z)

        returnData.append(newEntry)
    return returnData


def plotTracing(algorithmLabels, machineLabels, expectedLabels):
    fig = plt.figure()
    ax = Axes3D(fig)

    if algorithmLabels != None:
        simple = np.asarray(processLabels(algorithmLabels))
        ax.scatter(simple[:,0], simple[:,1], simple[:,2], marker = 'o', color = 'r')

    if machineLabels != None:
        complicated = np.asarray(processLabels(machineLabels))
        ax.scatter(complicated[:,0], complicated[:,1], complicated[:,2], marker = '.', color = 'b')
    
    if expectedLabels != None:
        expected = np.asarray(processLabels(expectedLabels))
        ax.scatter(expected[:,0], expected[:,1], expected[:,2], marker = 'x', color = 'k')
    
    ax.scatter(0,0,0, marker = '.', color = 'k')
    
    plt.show()