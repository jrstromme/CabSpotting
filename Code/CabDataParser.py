'''
CabDataParser.py

By: John Stromme
05/07/14

Main File

runs all of the data parsing/organizing necessary

'''
import rawDataParser
import ShapelyRemoveOutsideSF
import arcGISParser


rawDataDirectory = "/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/cabs"
outputDirectory = "/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/output/"
coordDirectory = "/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/"

def main():
    
    #1 Parse Raw Data using TaxiParse (add ID capabilities)
    rawDataParser.parseRawData(rawDataDirectory,outputDirectory,'initialParse.csv')

    #2 Eliminate irrelevant dataPoints based on shapely (ShapelyRemoveOutliers)
    ShapelyRemoveOutsideSF.removeDataOutsideSF(outputDirectory,'initialParse.csv','cabTripData.csv',coordDirectory,"SFCoordinateLimits.csv",True)

    #3 Organize into ArcGis format with IDs
    arcGISParser.parseForArcGIS(outputDirectory, 'cabTripData.csv', outputDirectory, 'arcGISParse.csv')  

main()

