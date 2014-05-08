'''

Parses downloaded google data

'''
import pickle
import csv

'''
setup files to open/read
'''



writeFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/pubTransAlt.txt','w')

with open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/bartFareTableSF.csv','r') as bartFareCSV:
	bartFareMatrix = [row for row in csv.reader(bartFareCSV.read().splitlines())]

'''
FUNCTIONS
'''
stationList = ['Daly City', 'Balboa Park', 'Glen Park', '24th St. Mission', '16th St. Mission',	
	          'Civic Center/UN Plaza', 'Powell St.', 'Montgomery', 'Embarcadero']

def getBartIndex(stationName):
	for i in range(len(stationList)):
		if stationName == stationList[i]:
			return i+1
	return 0
	
def getBartFare(origin, destination):
	originIndex = getBartIndex(origin)
	destinationIndex = getBartIndex(destination)
	return bartFareMatrix[originIndex][destinationIndex]
		
	
def parseTransitData(tripsList):
	#initialize variables
	lst = []
	
	#distance
	walkingDistance = 0
	busDistance = 0
	cableDistance = 0
	bartDistance = 0
	metroDistance = 0
	
	#misc
	numTransfers = 0
	travelTime = 0
	busUsed = False
	metroUsed = False
	
	
	
	tripnum = 0
	
	for item in tripsList:
		tripnum = tripnum + 1
		#initialize variables
		
		busDistance = 0
		busTime = 0
		
		bartDistance = 0
		bartTime = 0
		bartCost = 0
		
		railDistance = 0
		railTime = 0
		
		cableDistance = 0
		cableTime = 0
		
		walkingDistance = 0
		walkingTime = 0
		
		numTransfers = 0
		totalTime = 0
		totalDistance = 0
		totalPrice = 0
		
		metroIndicator = 0
		cableIndicator = 0
		
		otherModes = []
		
	
		
		for leg in item[0]['routes'][0]['legs'][0]['steps']:
			if leg['travel_mode']=='TRANSIT':
				if leg['transit_details']['line']['vehicle']['name'] == 'Bus':
					busDistance = busDistance + leg['distance']['value']
					busTime = busTime + leg['duration']['value']
					metroIndicator=1
				elif leg['transit_details']['line']['vehicle']['name'] == 'Light rail':
					railDistance = railDistance + leg['distance']['value']
					railTime = railTime + leg['duration']['value']
					metroIndicator = 1
				elif leg['transit_details']['line']['vehicle']['name'] == 'Cable car':
					cableDistance = cableDistance + leg['distance']['value']
					cableTime = cableTime + leg['duration']['value']
					cableIndicator = 1
				elif leg['transit_details']['line']['vehicle']['name'] == 'Metro rail':
					if leg['transit_details']['line']['agencies'][0]['name'] == 'Bay Area Rapid Transit':
						bartDistance = bartDistance + leg['distance']['value']
						bartTime = bartTime + leg['duration']['value']
						#cost algorithm to be implemented later- need origin station and destination station
						originStation = leg['transit_details']['departure_stop']['name']
						destinationStation = leg['transit_details']['arrival_stop']['name']
						bartCost = float(getBartFare(originStation, destinationStation))
					else:
						otherModes.append(leg['transit_details']['line']['agencies'][0]['name'])
				else:
					otherModes.append(leg['transit_details']['line']['vehicle']['name'])
			elif leg['travel_mode']=='WALKING': 
				walkingDistance = walkingDistance + leg['distance']['value']
				walkingTime = walkingTime + leg['duration']['value']
			else:
				otherModes.append(leg['travel_mode'])
		totalTime = busTime + bartTime + railTime + cableTime + walkingTime
		totalDistance = busDistance + bartDistance + railDistance + cableDistance + walkingDistance
		totalPrice = 2*metroIndicator + 6*cableIndicator + bartCost
		#write file is .csv format with columns
		#originArea, destinationArea, busDistance, busTime, BARTDistance, BARTTime, BARTCost,
							#railDistance, railTime, cableDistance, cableTime, walkingDistance, walkingTime
							#numTransfers, totalTime, totalDistance
		writeFile.write(item[1] + ',' + item[2] + ',' + str(busDistance) + ',' + str(busTime) + ',' + str(bartDistance) +
			',' + str(bartTime) + ',' + str(bartCost) + ',' + str(railDistance) + ',' + str(railTime) + 
			',' + str(cableDistance) + ',' + str(cableTime) + ',' + str(walkingDistance) + ',' + str(numTransfers) +
			',' + str(totalTime) + ',' + str(totalDistance) + ',' + str(totalPrice) + '\r')
		print(totalPrice)
		
	print otherModes
	
def runParserOnObject(pickledObjectFile):		
	filehandler = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/' + pickledObjectFile,'r')
	transitList = pickle.load(filehandler)
	parseTransitData(transitList)

runParserOnObject('directions204741164463.obj')


