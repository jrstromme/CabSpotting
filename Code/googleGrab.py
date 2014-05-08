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
		


'''


import requests
import json
import csv
import pickle
import datetime




'''
Main Code
'''



with open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/areaCentroids.csv','r') as areaCentroidsFile:
	data = [row for row in csv.reader(areaCentroidsFile.read().splitlines())]	
	for i in range(len(data)-1):
		if i==0:
			for j in range(len(data[i])):
				if data[i][j]=='latitude':
					latitudeIndex = j
				elif data[i][j]=='longitude':
					longitudeIndex = j
				elif data[i][j]=='area':
					areaIndex = j
		else:
			area1 =  str(data[i][latitudeIndex]) + ',' + str(data[i][longitudeIndex])
			k=i+1
			for k in range(i+1,len(data)):
				area2 = str(data[k][latitudeIndex]) + ',' + str(data[k][longitudeIndex])
				time = str(1395289999)
				url1 = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + area1 + '&destination=' + area2 +  '&sensor=false&mode=transit&departure_time=' + time + "&key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU"
				url2 = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + area2 + '&destination=' + area1 +  '&sensor=false&mode=transit&departure_time=' + time + "&key=AIzaSyBAPiVO2a0q7YMThYS-Begdw6GtIwLKgFU"
				lst.append([json.loads(requests.get(url1).text),data[i][areaIndex],data[k][areaIndex]])
				lst.append([json.loads(requests.get(url2).text),data[k][areaIndex],data[i][areaIndex]])


lstFile = open('/Users/John/Documents/Carleton/Academia/Econ/Comps/Data/cabspottingdata/directions' + str(datetime.datetime.now().time()) + '.obj', 'w')
pickle.dump(lst, lstFile)







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

































