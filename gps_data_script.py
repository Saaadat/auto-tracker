import urllib2
import time
import serial
import random
import compassbearing as cp
import math

def raw_data():

    try:
        #response = urllib2.urlopen('http://192.168.37.1:56781/mavlink/')
        response = urllib2.urlopen('http://127.0.0.1:56781/mavlink/')
        page_source = response.read()
        #print page_source
        alt = 'alt'
        lat = 'lat'
        lon = 'lon'
        speed = 'groundspeed'
        heading = 'heading'

        index0 = page_source.find(alt)
        index1 = page_source.find(lat)
        index2 = page_source.find(lon)
        index3 = page_source.find(speed)
        index4 = page_source.find(heading)

        alt_raw = page_source[index0:]
        lat_raw = page_source[index1:]
        lon_raw = page_source[index2:]
        speed_raw = page_source[index3:]
        heading_raw = page_source[index4:]

        index5 = alt_raw.find(',')
        index6 = lat_raw.find(',')
        index7 = lon_raw.find(',')
        index8 = speed_raw.find(',')
        index9 = heading_raw.find(',')

        alt_raw = alt_raw[:index5]
        lat_raw = lat_raw[:index6]
        lon_raw = lon_raw[:index7]
        speed_raw = speed_raw[:index8]
        heading_raw = heading_raw[:index9]

        index10 = alt_raw.find(':')
        index11 = lat_raw.find(':')
        index12 = lon_raw.find(':')
        index13 = speed_raw.find(':')
        index14 = heading_raw.find(':')
        
        alt = alt_raw[index10+1:]
        lat = lat_raw[index11+1:]
        lon = lon_raw[index12+1:]
        speed = speed_raw[index13+1:]
        heading = heading_raw[index14+1:]

    except urllib2.URLError, e:
        alt, lat, lon, speed, heading = float(0),float(0),float(0),float(0),float(0)
        

    return alt, lat, lon, speed, heading

def azimuth(lat1,lon1,lat2,lon2):
    
    current_coord = (lat1, lon1)
    coord2 = (lat2,lon2)
    diff1 = -(current_coord[0] - coord2[0])
    diff2 = -(current_coord[1] - coord2[1])
    
    azimuth = cp.calculate_initial_compass_bearing(current_coord,coord2)

    return azimuth

def bearing(azimuth):

    azimuth = int(azimuth)

    if azimuth >= 0 and azimuth <= 90:
        bearing = str('N ' + str(azimuth) + ' E')
    elif azimuth >90 and azimuth <= 180:
        bearing = str('S ' + str(180-azimuth) + ' E')
    elif azimuth >180 and azimuth <= 270:
        bearing = str('S ' + str(azimuth-180) + ' W')
    elif azimuth >270 and azimuth <= 360:
        bearing = str('N ' + str(360-azimuth) + ' W')

    return bearing

def distance(lat1, lon1, lat2, lon2):
    
    r = 6371
    w = math.radians(lat1)
    x = math.radians(lat2)
    y = math.radians(lat2-lat1)
    z = math.radians(lon2-lon1)

    a = (math.sin(y/2) * math.sin(y/2)) + (math.cos(w) * math.cos(x) * (math.sin(z/2) * math.sin(z/2)))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = (r * c )

    return d
    
    

def main():
    alt, lat, lon, speed, heading = raw_data()
    print alt, lat, lon, speed, heading
        
if __name__ == '__main__':
    main()
    










        
        
