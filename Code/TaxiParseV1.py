'''
Taxi Parser

This python script will parse taxi GPS data into a smaller file which contains a list
of trips a taxi has taken with beginning and ending coordinates. It also will compute
the total distance traveled

V1:Only parses beginning and ending coordinates/time

'''
import glob
import os
import datetime

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
    beginningUnixTime = 0
    beginningTime = ''
    endingCoordinates = []
    
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
                beginningIndicator=0
                wFile.write(str(beginningCoordinates[0]) + "," + str(beginningCoordinates[1])
                 + "," + str(endingCoordinates[0]) + "," + str(endingCoordinates[1]) + ","
                 + str(beginningUnixTime) + "," + str(beginningTime) + "," + str(tripCount) 
                 + "\r")
                tripCount = tripCount + 1
        if beginningIndicator==0:
            if dataList[2] == "1":
                beginningIndicator = 1
                beginningCoordinates = [dataList[0],dataList[1]]
                beginningUnixTime = dataList[3]
                beginningTime = datetime.datetime.fromtimestamp(int(dataList[3])).strftime('%H')

        prevLineData = dataList


for file in fileList:
    parseCabFile(file,'writeTest.txt',"/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs/")
            