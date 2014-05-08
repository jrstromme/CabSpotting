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

wFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/shapelyTestOutput.txt','w')

def getPolygon(row,coordinateDir,coordinateFileName):
	
polygonData = openCSVFile('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/SFCoordinateLimits.csv')
UTM1 = utm.from_latlon(float(polygonData[1][0]),float(polygonData[1][1]))
UTM1 = [UTM1[0],UTM1[1]]
UTM2 = utm.from_latlon(float(polygonData[1][2]),float(polygonData[1][3]))
UTM2 = [UTM2[0],UTM2[1]]
UTM3 = utm.from_latlon(float(polygonData[1][4]),float(polygonData[1][5]))
UTM3 = [UTM3[0],UTM3[1]]
UTM4 = utm.from_latlon(float(polygonData[1][6]),float(polygonData[1][7]))
UTM4 = [UTM4[0],UTM4[1]]
SFpolygon = Polygon([(UTM1[0],UTM1[1]),(UTM2[0],UTM2[1]),(UTM3[0],UTM3[1]),(UTM4[0],UTM4[1])])
print(SFpolygon.area)
UTM1 = utm.from_latlon(float(polygonData[2][0]),float(polygonData[2][1]))
UTM1 = [UTM1[0],UTM1[1]]
UTM2 = utm.from_latlon(float(polygonData[2][2]),float(polygonData[2][3]))
UTM2 = [UTM2[0],UTM2[1]]
UTM3 = utm.from_latlon(float(polygonData[2][4]),float(polygonData[2][5]))
UTM3 = [UTM3[0],UTM3[1]]
UTM4 = utm.from_latlon(float(polygonData[2][6]),float(polygonData[2][7]))
UTM4 = [UTM4[0],UTM4[1]]
cabLotPolygon = Polygon([(UTM1[0],UTM1[1]),(UTM2[0],UTM2[1]),(UTM3[0],UTM3[1]),(UTM4[0],UTM4[1])])
print(cabLotPolygon.area)

initialize=1
with open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/TaxiParseV4.csv', 'rb') as csvfile:
	for line in csv.reader(csvfile.read().splitlines()):
		if initialize==0:
			point1 = Point(float(line[4]),float(line[5]))
			point2 = Point(float(line[6]),float(line[7]))
			if SFpolygon.contains(point1)==True and SFpolygon.contains(point2)==True:
				if cabLotPolygon.contains(point1)==False and cabLotPolygon.contains(point2)==False:
					for item in line:
						wFile.write(item + ',')
					wFile.write('\r')
		else:
			initialize=0	
			

def removeDataOutsideSF(outputDir,inputFileName,outputFileName,coordinateDir,coordinateFileName):
	 

#print(polygon.contains(a))