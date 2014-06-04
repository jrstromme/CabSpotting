'''
Retrieves directions information from Google Maps API

FROM GOOGLE's DOCUMENTATION
A Directions API request takes the following form:

http://maps.googleapis.com/maps/api/directions/output?parameters
where output may be either of the following values:

json (recommended) indicates output in JavaScript Object Notation (JSON)
xml indicates output as XML

Data Structure: ----
	under ['routes'][0]['legs'][0] - each leg of the trip is an index, (leg=waypoint to waypoint)
Steps contains information on each step
	distance - total trip distance in miles or meters
	duration - total time of trip
		
		
key 1: key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU
key 2: key=AIzaSyD256_wOceWKnrLbu5Pmwx5ixIsDc-zoU0
key 3: key=AIzaSyAV07bp3KDBIleZ7K1_bfRhoEKLAHwmLJE

'''


import requests
import json
import csv
import pickle
import datetime
import calendar
import sys




'''
Main Code
'''
#1401908400


with open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/areaCentroids.csv','r') as areaCentroidsFile:
	departureTime = datetime.datetime.fromtimestamp(1401926400)
	#departureTime = dateTime - datetime.datetime.fromtimestamp(0)
	time = str(calendar.timegm(departureTime.utctimetuple()))
	lst = []
	data = [row for row in csv.reader(areaCentroidsFile.read().splitlines())]	
	counter = 0
	resumei = 24
	for i in range(resumei,len(data)-1):
		if i==resumei:
			for j in range(len(data[0])):
				if data[0][j]=='INTPTLAT':
					latitudeIndex = j
				elif data[0][j]=='INTPTLON':
					longitudeIndex = j
				elif data[0][j]=='NAME':
					areaIndex = j
		else:
			area1 =  str(data[i][latitudeIndex]) + ',' + str(data[i][longitudeIndex])
			k=i+1
			for k in range(i+1,len(data)):
				area2 = str(data[k][latitudeIndex]) + ',' + str(data[k][longitudeIndex])
				url1 = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + area1 + '&destination=' + area2 +  '&sensor=false&mode=transit&departure_time=' + time + "&key=AIzaSyBpRGckeBBuIpzOqUj5grLF5h58krsRx9U"
				url2 = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + area2 + '&destination=' + area1 +  '&sensor=false&mode=transit&departure_time=' + time + "&key=AIzaSyBpRGckeBBuIpzOqUj5grLF5h58krsRx9U"
				if counter*4 > 756 :
					print url1
					print "exceeded limit, stopped on row" + str(i)
					lstFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/directions' + str(datetime.datetime.now().time()) + '.obj', 'w')
					pickle.dump(lst, lstFile)
					sys.exit()
				else:
					lst.append([json.loads(requests.get(url1).text),data[i][areaIndex],data[k][areaIndex]])
					lst.append([json.loads(requests.get(url2).text),data[k][areaIndex],data[i][areaIndex]])
					counter += 1
				print counter
				










'''

OLD PRINTING EDA CODE

https://maps.googleapis.com/maps/api/directions/json?37.808058,-122.475657&destination=37.770804,-122.477403&sensor=false&mode=transit&departure_time=1395289999&key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU
https://maps.googleapis.com/maps/api/directions/json?origin=37.721421,-122.447556&destination=37.755868,-122.414211&sensor=false&mode=transit&departure_time=1395289999&key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU
r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=37.721421,-122.447556&destination=37.755868,-122.414211&sensor=false&mode=transit&departure_time=1395289999&key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU',verify=True)
j = json.loads(r.text)


print j['routes'][0]['legs'][0]['steps']
for leg in j['routes'][0]['legs'][0]['steps']:
	#print leg['travel_mode'] + leg['duration']
	print leg['travel_mode']
	print "duration in minutes " + str(leg['duration']['value'])
	print "distance in meters " + str(leg['distance']['value'])
	if leg['travel_mode']=='TRANSIT':
		print leg['transit_details']['line']['vehicle']['name']
		print leg['transit_details']['line']['agencies'][0]['name']
	print '\r'

'''

































