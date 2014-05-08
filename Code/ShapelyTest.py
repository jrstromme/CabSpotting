'''
Code reads in polygon coordinates from a .csv file
tests whether points exist in each polygon

'''


from shapely.geometry import Polygon
from shapely.geometry import Point
import csv
import utm
import pickle

wFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/shapelyTestOutput.txt','w')

def openCSVFile(filePath):
    with open(filePath,'r') as csvFile:
        data = [row for row in csv.reader(csvFile.read().splitlines())]
    return data

def parseAreasIntoShapely():
    centroidWFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/areaCentroids.txt','w')
    polygonData = openCSVFile('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/areaCoordinates.csv')
    initialize=1
    polygonList = []
    for line in polygonData:
        if initialize==1:
            initialize=0
        else:
            UTM1 = utm.from_latlon(float(line[0]),float(line[1]))
            UTM1 = [UTM1[0],UTM1[1]]
            UTM2 = utm.from_latlon(float(line[2]),float(line[3]))
            UTM2 = [UTM2[0],UTM2[1]]
            UTM3 = utm.from_latlon(float(line[4]),float(line[5]))
            UTM3 = [UTM3[0],UTM3[1]]
            UTM4 = utm.from_latlon(float(line[6]),float(line[7]))
            UTM4 = [UTM4[0],UTM4[1]]
            polygon = Polygon([(UTM1[0],UTM1[1]),(UTM2[0],UTM2[1]),(UTM3[0],UTM3[1]),(UTM4[0],UTM4[1])])
            areaNum = int(line[8])
            polygonList.append([polygon,areaNum])
            centroid = polygon.centroid
            centroidCoord = utm.to_latlon(polygon.centroid.x,polygon.centroid.y,10,'S')
            centroidWFile.write(line[8] + ',' + str(centroidCoord[0]) + ',' + str(centroidCoord[1]) + '\r')
    polygonFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/' + 'polygonList' + '.obj', 'w')
    pickle.dump(polygonList, polygonFile)
    return polygonList


def createEmptyListStructure(numAreas):
    lst = []
    for i in range(numAreas):
        lst.append([])
        for j in range(numAreas):
            lst[i].append(0)
    return lst

def assignCoordToBins(filePath,numAreas):
    areaCounts = createEmptyListStructure(numAreas)
    wFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/areaCounts.txt','w')
    errorFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/ridesOutOfAreas.txt','w')
    fileHandler = open(filePath,'r')
    polygonList = pickle.load(fileHandler)
    with open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/TaxiParseV3.csv', 'rb') as csvfile:
        for line in csv.reader(csvfile.read().splitlines()):
            origin = Point(float(line[4]),float(line[5]))
            destination = Point(float(line[6]),float(line[7]))
            originAreaIndex = -1
            destinationAreaIndex = -1
            for polygon in polygonList:
                if polygon[0].contains(origin)==True:
                    originAreaIndex = polygon[1]
            for polygon in polygonList:
                if polygon[0].contains(destination)==True:
                    destinationAreaIndex = polygon[1]
            if originAreaIndex ==-1 | destinationAreaIndex==-1:
            	for i in line:
            		errorFile.write(i + ',')
            	errorFile.write('\r')
            else:
            	areaCounts[originAreaIndex][destinationAreaIndex] = areaCounts[originAreaIndex][destinationAreaIndex] + 1
    for i in range(len(areaCounts)):
        for j in range(len(areaCounts[i])):
            wFile.write(str(i+1) + ',' + str(j+1) + ',' + str(areaCounts[i][j]) + '\r')
    
                
parseAreasIntoShapely()
assignCoordToBins('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/' + 'polygonList' + '.obj',8)