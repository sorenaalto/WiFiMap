#!/usr/bin/env python

import requests
import urllib
import pprint
import csv

with open('WiFiHotspotsIn.csv','r') as f:
	csvin = csv.reader(f)
	rows = []
	for row in csvin:
		rows.append(row)

#print rows
	

pp = pprint.PrettyPrinter(indent=4)

def queryGmaps(q):
	key = "AIzaSyD1pqHX7tXb0uImEFMfYuQPyufALSl3EKE"
	parms = {'key':key,'query':q}
	encparms = urllib.urlencode(parms)
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?%s" % (encparms)

	r = requests.get(url)
	js = r.json()
	print "queryGmaps",q,url,js
	return js

def flushOutput():
	with open('WiFiHotspotsGPS.csv','w') as f:
		csvout = csv.writer(f)
		for row in rows:
			csvout.writerow(row)

for i in range(2,len(rows)):
	row = rows[i]
	#
	# check if there's already coordinates...
	if len(row)>6:
		lat = row[7]
		lng = row[8]
		if lat != '' or lng != '':
			print "Skipping lat/lng=",lat,lng
			continue

	query = "%s, %s, %s" % (row[2],row[4],row[1])
	print query

	js = queryGmaps(query)
	if js['status'] == 'OK':
		res = js['results']
#		pp.pprint(res)
		geo = res[0]['geometry']
#		pp.pprint(geo)
		loc = geo['location']
		pp.pprint(loc)
		row.append(loc['lat'])
		row.append(loc['lng'])
	else:
		query2 = "%s, %s" % (row[4],row[1])
		js = queryGmaps(query2)
		if js['status'] == 'OK':
			res = js['results']
#			pp.pprint(res)
			geo = res[0]['geometry']
#			pp.pprint(geo)
			loc = geo['location']
			pp.pprint(loc)
			row.append(loc['lat'])
			row.append(loc['lng'])
		else:
			print "I GIVE UP..."
	print "row=",row
	flushOutput()

