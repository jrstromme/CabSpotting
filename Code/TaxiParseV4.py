'''
Taxi Parser

This python script will parse taxi GPS data into a smaller file which contains a list
of trips a taxi has taken with beginning and ending coordinates. It also will compute
the total distance traveled

V1:Only parses beginning and ending coordinates/time
V2:Calculates distance of each taxi trip in kilometers as well as total trip time
V3:Converts GPS coordinates to DTM coordinates as well
V4:Cleans some data as the code runs. Realized data is read in reverse chronological order, reversed
	origin and destination logic

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
def parseCabFile (cabFile, wFile, dir):
    file = open(dir+cabFile, "r")
    
    beginningIndicator = 0
    prevLineData = []
    tripCount = 0
    originCoordinates = []
    originUTM = 0
    originUnixTime = 0
    originTime = ''
    destinationCoordinates = []
    destinationUTM = 0
    destinationUnixTime = 0
    destinationTime = ''
    
    tripDistance = 0
    tripTime = 0
    endOfFile=False
    
    while endOfFile == False:
        line = file.readline()
        if not line:
            endOfFile = True
        else:   
            dataList = [] 
            for token in line.split():
                dataList.append(token)

            if beginningIndicator==1:
                if dataList[2] == "0":
                    if tripDistance > .05:
                    #if tripDistance > 0:
                    	originUnixTime = prevLineData[3]
                        tripTime = datetime.timedelta(seconds=(int(destinationUnixTime)-int(originUnixTime)))
                        originTime = datetime.datetime.fromtimestamp(int(prevLineData[3])).strftime('%H')
                        if tripTime.total_seconds() > 60 and tripTime.total_seconds() < 10800:
                        #if tripTime.total_seconds() > 0:
                            originCoordinates = [prevLineData[0], prevLineData[1]]
                            originUTM = utm.from_latlon(float(originCoordinates[0]),float(originCoordinates[1]))
                            originUTM = [originUTM[0],originUTM[1]]
                            wFile.write(str(originCoordinates[0]) + "," + str(originCoordinates[1]) + ","
                             + str(destinationCoordinates[0]) + "," + str(destinationCoordinates[1]) + ","
                             + str(originUTM[0]) + "," + str(originUTM[1]) + "," +
                             str(destinationUTM[0]) + "," + str(destinationUTM[1]) + ","
                             + str(originUnixTime) + "," + str(destinationUnixTime) + "," 
                             + str(originTime) + "," + str(tripTime.total_seconds())
                             + "," + str(tripCount) + "," + str(tripDistance) + "\r")
                            tripCount = tripCount + 1
                    beginningIndicator=0
                    tripDistance = 0
                elif prevLineData:
                    tempDistance = haversine(float(prevLineData[0]),float(prevLineData[1]),float(dataList[0]),float(dataList[1]))
                    tempTime = (float(prevLineData[3])-float(dataList[3]))/3600
                    if tempDistance/tempTime < 100:
                        tripDistance = tripDistance + tempDistance

        
            if beginningIndicator==0:
                if dataList[2] == "1":
                    beginningIndicator = 1
                    tripDistance = 0
                    destinationCoordinates = [dataList[0],dataList[1]]
                    destinationUTM = utm.from_latlon(float(dataList[0]),float(dataList[1]))
                    destinationUTM = [destinationUTM[0],destinationUTM[1]]
                    destinationUnixTime = dataList[3]
                    destinationTime = datetime.datetime.fromtimestamp(int(dataList[3])).strftime('%H')
    
            prevLineData = dataList



def main():
    wFile = open("/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/TaxiParseV4.csv", "w")
    wFile.write("LatO,LonO,LatD,LonD,DTMLatO,DTMlonO,DTMLatD,DTMLonD,UnixStart,UnixEnd,HrStart,Duration,tripCount,Distance\r")
    for file in fileList:
       parseCabFile(file,wFile,"/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/")
    #parseCabFile('new_abboip.txt',wFile,"/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/")
        

def parseRawData(rawDataDir,outputDir,outputFileName):
	        
        
main()
            