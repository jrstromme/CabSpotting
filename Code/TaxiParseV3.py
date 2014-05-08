'''
Taxi Parser

This python script will parse taxi GPS data into a smaller file which contains a list
of trips a taxi has taken with beginning and ending coordinates. It also will compute
the total distance traveled

V1:Only parses beginning and ending coordinates/time
V2:Calculates distance of each taxi trip in kilometers as well as total trip time
V3:Converts GPS coordinates to DTM coordinates as well

'''
import glob
import os
import datetime
from math import radians, cos, sin, asin, sqrt
import utm

#This function calculates the distance between to gps coordinate points
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km


os.chdir("/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs")

fileList=[]

#find all taxi files
for file in glob.glob("*.txt"):
    fileList.append(file)

#function which parses each cab file down into starting and ending coordinates
def parseCabFile (cabFile, writeFile, dir):
    file = open(dir+cabFile, "r")
    wFile = open(writeFile, "a")
    
    beginningIndicator = 0
    prevLineData = []
    tripCount = 0
    beginningCoordinates = []
    beginningUTM = 0
    beginningUnixTime = 0
    beginningTime = ''
    endingCoordinates = []
    endingUTM = 0
    tripDistance = 0
    tripTime = 0
    pointCount = 0
    
    while 1:
        line = file.readline()
        if not line:
            break
        dataList = [] 
        for token in line.split():
            dataList.append(token)
        if beginningIndicator==1:
            if dataList[2] == "0":
                endingCoordinates = [prevLineData[0], prevLineData[1]]
                endingUTM = utm.from_latlon(float(endingCoordinates[0]),float(endingCoordinates[1]))
                endingUTM = [endingUTM[0],endingUTM[1]]
                tripTime = datetime.timedelta(seconds=(int(beginningUnixTime)-int(prevLineData[3])))                
                wFile.write(str(beginningCoordinates[0]) + "," + str(beginningCoordinates[1]) + ","
                 + str(endingCoordinates[0]) + "," + str(endingCoordinates[1]) + ","
                 + str(beginningUTM[0]) + "," + str(beginningUTM[1]) + "," +
                 str(endingUTM[0]) + "," + str(endingUTM[1]) + ","
                 + str(beginningUnixTime) + "," + str(beginningTime) + "," + str(tripTime)
                 + "," + str(tripCount) + "," + str(tripDistance) + ',' + str(pointCount) + ',' + cabFile + "\r")
                
                tripCount = tripCount + 1
                beginningIndicator=0
                tripDistance = 0
                pointCount = 0
                
        if prevLineData:
            tempDistance = haversine(float(prevLineData[0]),float(prevLineData[1]),float(dataList[0]),float(dataList[1]))
            tempTime = (float(prevLineData[3])-float(dataList[3]))/3600
            if tempDistance/tempTime < 100:
            	tripDistance = tripDistance + haversine(float(prevLineData[0]),float(prevLineData[1]),float(dataList[0]),float(dataList[1]))
            	pointCount = pointCount + 1

            
        if beginningIndicator==0:
            if dataList[2] == "1":
                beginningIndicator = 1
                tripDistance = 0
                pointCount = 0
                beginningCoordinates = [dataList[0],dataList[1]]
                beginningUTM = utm.from_latlon(float(dataList[0]),float(dataList[1]))
                beginningUTM = [beginningUTM[0],beginningUTM[1]]
                beginningUnixTime = dataList[3]
                beginningTime = datetime.datetime.fromtimestamp(int(dataList[3])).strftime('%H')

        prevLineData = dataList




for file in fileList:
    parseCabFile(file,'writeTest.csv',"/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/")
#parseCabFile('new_aldhidd.txt','writeTest.csv',"/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/")