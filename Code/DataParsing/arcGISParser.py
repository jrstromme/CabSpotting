'''
arcGISParser.py

'''
import csv


def parseForArcGIS(inputDir, inputFileName, outputDir, outputFileName):
    
    endOfFile = False
    file = open(inputDir+inputFileName, "r")
    outputFile = open(outputDir+outputFileName, "w")
    initialize = 1
    for line in csv.reader(file.read().splitlines()):
        if initialize == 1:
            outputFile.write(line[0] + ',' + line[1] + ',' + line[14] + '\r')
            initialize = 0
        elif initialize == 0:
            outputFile.write(line[0] + ',' + line[1] + ',' + line[14] + '\r')
            outputFile.write(line[2] + ',' + line[3] + ',' + line[14] + '\r')