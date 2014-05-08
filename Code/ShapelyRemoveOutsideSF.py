'''
Code reads in polygon coordinates from a .csv file
tests whether points exist in each polygon

'''


from shapely.geometry import Polygon
from shapely.geometry import Point
import csv
import utm



def openCSVFile(filePath):
    with open(filePath,'r') as csvFile:
        data = [row for row in csv.reader(csvFile.read().splitlines())]
    return data

def getPolygon(row,coordinateDir,coordinateFileName):
    polygonData = openCSVFile(coordinateDir+coordinateFileName)   
    UTM1 = utm.from_latlon(float(polygonData[row][0]),float(polygonData[row][1]))
    UTM1 = [UTM1[0],UTM1[1]]
    UTM2 = utm.from_latlon(float(polygonData[row][2]),float(polygonData[row][3]))
    UTM2 = [UTM2[0],UTM2[1]]
    UTM3 = utm.from_latlon(float(polygonData[row][4]),float(polygonData[row][5]))
    UTM3 = [UTM3[0],UTM3[1]]
    UTM4 = utm.from_latlon(float(polygonData[row][6]),float(polygonData[row][7]))
    UTM4 = [UTM4[0],UTM4[1]]
    return Polygon([(UTM1[0],UTM1[1]),(UTM2[0],UTM2[1]),(UTM3[0],UTM3[1]),(UTM4[0],UTM4[1])])


def testGPSPoints(polygons, points, header,outputDir,inputFileName,outputFileName):
    ID = 0
    outputFile = open(outputDir + outputFileName,'w')
    if header == True:
        initialize=1
    elif header == False:
        initialize=0
    else:
        print "Specify header as True or False"
        
    with open(outputDir + inputFileName, 'rb') as csvfile:
        for line in csv.reader(csvfile.read().splitlines()):
            if initialize==0:
                point1 = Point(float(line[4]),float(line[5]))
                point2 = Point(float(line[6]),float(line[7]))
                keepPoint = True
                for i in range(len(polygons)):
                    if testPolygon(polygons[i], points[i], point1, point2)==False:
                        keepPoint = False
                if keepPoint == True:
                    for item in line:
                        outputFile.write(item + ',')
                    outputFile.write(str(ID))
                    ID = ID + 1
                    outputFile.write('\r')
            else:
                initialize=0    
                for item in line:
                    outputFile.write(item + ',')
                outputFile.write('ID')
                outputFile.write('\r')    

def testPolygon(polygon, points, point1, point2):
    if points == 'inside':
        keep = True
    elif points == 'outside':
        keep = False
    else:
        'need to specify whether to keep inside points or outside points'
                        
    if polygon.contains(point1) == keep and polygon.contains(point2) == keep:
        return True
    else:
        return False

            

def removeDataOutsideSF(outputDir,inputFileName,outputFileName,coordinateDir,coordinateFileName,header):
     SFpolygon = getPolygon(1,coordinateDir,coordinateFileName)
     cabLotPolygon = getPolygon(2,coordinateDir,coordinateFileName)
     
     testGPSPoints([SFpolygon,cabLotPolygon],['inside','outside'],header, outputDir, inputFileName, outputFileName)

#print(polygon.contains(a))