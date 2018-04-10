import urllib
import io

def currentmap(lat,lon):
    URL = 'http://maps.googleapis.com/maps/api/staticmap?center=' + str(lat) + ',' + str(lon) + '&markers=' +str(lat)+ ',' +str(lon) + '&zoom=15&size=400x300&sensor=false&key=AIzaSyCyz-rUpyK53la1Xn5QFA6CpgpUwNEJZBM'
    #URL = 'http://127.0.0.1:56781/hud.jpg'
    x = urllib.urlopen(URL)
    with open('tempt.png', 'wb') as f:
        f.write(x.read())
        f.close()
