# import urllib2
# import json
url = "https://api.foursquare.com/v2/venues/search?client_id=Z41TKJBJASCF5D1PYQFHGK2KEYIKS5IHJMT5FBNWVACEAEVY&client_secret=DN5TYLFK2T1RZ5PAX1YA2ERDLC0ASXLXDOXEM3B43IDPURCY&ll=35.7090259,139.7319925&v=20130815 &query='Pizza'"
# req = urllib2.Request(url)
# opener = urllib2.build_opener()
# # print "===", req
# f = opener.open(req)
# json = json.loads(f.read())
# print json
# print json['meta']


import urllib, json
# url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data['meta']