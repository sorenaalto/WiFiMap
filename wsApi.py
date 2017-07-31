#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
from wifigpsutil import WiFiInfo

app = Flask(__name__)
api = Api(app)

wifilist = WiFiInfo()

search_args = {
	'lat0' : fields.Float(),
	'lng0' : fields.Float(),
	'lat1' : fields.Float(),
	'lng1' : fields.Float()
}

class WiFi(Resource):
	@use_args(search_args)
	def get(self,args):
		print "args=",args
		homelat = -29.8488718
		homelng = 31.0048382
		delta=0.005

#		hlist = wifilist.inBox(homelat-delta,homelng-delta,homelat+delta,homelng+delta)
		hlist = wifilist.inBox(args['lat0'],args['lng0'],args['lat1'],args['lng1'])
		rlist= []
		for h in hlist:
			rlist.append(h.__dict__)
		return rlist

api.add_resource(WiFi,'/WiFi')

@app.route('/map')
def show_map():
	return render_template("map.html",value='bazinga')

if __name__ == '__main__':
    app.run(debug=True,port=5050)
