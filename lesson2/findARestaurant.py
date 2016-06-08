# from geocode import getGeocodeLocation
import json
import httplib2
import urllib

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "Z41TKJBJASCF5D1PYQFHGK2KEYIKS5IHJMT5FBNWVACEAEVY"
foursquare_client_secret = "DN5TYLFK2T1RZ5PAX1YA2ERDLC0ASXLXDOXEM3B43IDPURCY"
versionParameter = "20130815"

def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    google_api_key = "AIzaSyBGOzhUHfOgQb6mbBuBxGuGNoKfWX6EZ0o"
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    # print "getGeocodeLocation"
    return (latitude,longitude)

def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	(lat, lon) = getGeocodeLocation(location)
	print lat, lon

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	# url = ('https://api.foursquare.com/v2/venues/search?client_id=%s &client_secret=%s &v=%s &ll=%d,%d &intent=browse &radius=80000 &query=%s '%(foursquare_client_id, foursquare_client_secret, versionParameter, lat, lon, mealType))
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s &client_secret=%s &v=%s &ll=%d,%d &query=%s '%(foursquare_client_id, foursquare_client_secret, versionParameter, lat, lon, mealType))
	response = urllib.urlopen(url)

	data = json.loads(response.read())
	# print data['response']['venues'][0]
	# print url
	# print data

	# numberOfRestaurant = len(data['response']['venues'])
	# print data['response']['venues'][0]
	restaurantDict = {}
	for i in xrange(len(data['response']['venues'])):
		#3. Grab the first restaurant
		restaurant = data['response']['venues'][i]

		# print type(response), type(data), type(restaurant)

		#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		# venue_id = data['response']['venues'][0]['id']
		venue_id = restaurant['id']

		photoJsonURL = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=%s '%(venue_id, foursquare_client_id, foursquare_client_secret, versionParameter))
		photoResponse = urllib.urlopen(photoJsonURL)
		photoData = json.loads(photoResponse.read())

		print photoJsonURL

		photoItems = photoData['response']['photos']['items']
		if photoItems != []:
			# print photoItems[0]["source"]
			prefix = photoItems[0]['prefix']
			suffix = photoItems[0]['suffix']
			imageURL = prefix + '300x300' + suffix
			# print imageURL
		else:
			# print "====No Image Found====" 
			imageURL = "====No Image Found====" 
		# for i in range(10):
		# 	venue_id = data['response']['venues'][i]['id']
		# 	print venue_id

		#5. Grab the first image

		#6. If no image is available, insert default a image url

		#7. Return a dictionary containing the restaurant name, address, and image url
		restaurantName = restaurant['name']
		restaurantAddress = ', '.join(restaurant['location']['formattedAddress'])
		print 'Restaurant Name:', restaurantName
		print 'Restaurant Address:', restaurantAddress
		print 'Image:', imageURL, '\n'
		restaurantDict[venue_id] = [restaurantName, restaurantAddress, imageURL]

	return restaurantDict
		
if __name__ == '__main__':
 	findARestaurant("Pizza", "Tokyo, Japan")
	# findARestaurant("Tacos", "Jakarta, Indonesia")
	# findARestaurant("Tapas", "Maputo, Mozambique")
	# findARestaurant("Falafel", "Cairo, Egypt")
	# findARestaurant("Spaghetti", "New Delhi, India")
	# findARestaurant("Cappuccino", "Geneva, Switzerland")
	# findARestaurant("Sushi", "Los Angeles, California")
	# findARestaurant("Steak", "La Paz, Bolivia")
	# findARestaurant("Gyros", "Sydney Australia")


