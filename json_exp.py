import urllib, json
url = "http://maps.googleapis.com/maps/api/geocode/json?address=google"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
