#!/usr/bin/env python

import csv

class HotspotInfo:
	def __init__(self):
		self.area = ""
		self.place = ""
		self.loctype = ""
		self.address = ""
		self.provider = ""
		self.timelimit = ""
		self.datalimit = ""
		self.extra = ""
		self.lat = 0.0
		self.lng = 0.0

	def fromRow(self,r):
		self.id = r[0]
		self.area = r[1]
		self.place = r[2]
		self.loctype = r[3]
		self.address = r[4]
		self.provider = r[5]
		self.timelimit = r[6]
		self.datalimit = r[7]
		self.extra = r[8]
		self.lat = float(r[9])
		self.lng = float(r[10])

	def __repr__(self):
		return str(self.__dict__)

class WiFiInfo:
	def __init__(self):
		filename = "WiFiHotspotsGPS.csv"
		with open(filename,'r') as f:
			self.rows = []
			self.hotspots = []
			csvin = csv.reader(f)
			for row in csvin:
				if(len(row)>9):
					self.rows.append(row)
					hsi = HotspotInfo()
					hsi.fromRow(row)
					# change the ID to match the index in the array
					hsi.id = len(self.hotspots)
					self.hotspots.append(hsi)

	def dist(self,hs,lat,lng):
		return abs(lat-hs.lat)+abs(lng-hs.lng)

	def nearestN(self,N,lat,lng):
		tuplist = []
		for hs in self.hotspots:
			d = self.dist(hs,lat,lng)
			tup = (d,hs)
			tuplist.append(tup)
		tuplist.sort(key=lambda k:k[0])	
		hslist = []
		for i in range(0,N):
			hs = tuplist[i][1]
			hslist.append(hs)
		return hslist

	def inBox(self,lat0,lng0,lat1,lng1):
		listout = []
		for hs in self.hotspots:
			if ( lat0 <= hs.lat and hs.lat <= lat1 ) \
				and \
				( lng0 <= hs.lng and hs.lng <= lng1 ):
				listout.append(hs)
		return listout

if __name__ == "__main__":
	wi = WiFiInfo()
#	print wi.hotspots

#	for hsi in wi.hotspots:
#		print wi.dist(hsi,-30.0,30.0)

	homelat = -29.8488718
	homelng = 31.0048382
	hlist = wi.nearestN(20,homelat,homelng)
	delta=0.005

	hlist = wi.inBox(homelat-delta,homelng-delta,homelat+delta,homelng+delta)
	for h in hlist:
		print h

