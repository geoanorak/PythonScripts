# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:18:32 2015

@author: Phil James @geoanorak
Plot wind directions using Basemap
Data from met office datapoint API
Needs API key substitute for dummy here
"""



import json
import urllib
import pylab as plt
from mpl_toolkits.basemap import Basemap
import math

#Get data from Met office API change date to get newer data
mojson = urllib.urlopen('http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/all?res=hourly&time=2015-03-20T12:00:00Z&key=xxxxxxxxxxxxxxxxxxxxxxxxxxx')

data = json.load(mojson)

#Convert json to lists
lat = []
lon= []
wdir = []
wspeed = []

rows = data['SiteRep']['DV']['Location']
for r in range(0, len(rows)):
    print "lat: ", rows[r]['lat'], rows[r]['lon']
    try:    
        dir= rows[r]['Period']['Rep']['D']
        print dir
        sp = rows[r]['Period']['Rep']['S']
        lat.append(float(rows[r]['lat']))
        lon.append(float(rows[r]['lon']))
        wdir.append(dir)
        wspeed.append(float(sp))
    except:
        print 'nodata'
    
#Sort out wind directions
dirs=['N','NNE', 'NE', 'ENE','E', 'ESE', 'SE','SSE','S', 'SSW', 'SW', 'WSW','W', 'WNW', 'NW', 'NNW']
#set up bearings
angs = range(0,720, 45)
for i in range(0, len(angs)):
    angs[i] = float(angs[i]) / 2

#lookup compass direction and get bearing - create dictionary
dirdict = dict(zip(dirs, angs))

#flips the directions by 180 (as wind is direction FROM not TO but arrows are direction TO)
windangs=[]
for i in range(0, len(lat)):
    try:
        val = dirdict[wdir[i]]
        val = val + 180
        if val>=360:
            val = val - 360
        windangs.append(val)
    except :
        windangs.append(0.0)


for i in range(0, len(lat)):
    print lat[i], lon[i], wdir[i], wspeed[i], windangs[i]

m = Basemap(llcrnrlon=-10.5,llcrnrlat=49.5,urcrnrlon=3.5,urcrnrlat=59.5,resolution='i',projection='tmerc',lon_0=-4.36,lat_0=54.7)
m.drawcoastlines()

minsize = 10000 #min size for arrow

#Plot the arrows on the map
for i in range(0, len(lon)):
    x,y = m(lon[i], lat[i])
    rad = math.radians(windangs[i])
    #adjust length based on wind speed
    if wspeed[0]>0:
        adj = 30000 * (wspeed[i]/100)
        arsize = minsize + adj
        dx = arsize * math.sin(rad)
        dy = arsize * math.cos(rad)
        if wspeed[i] > 25:
            col = "r"
        else:
            col = "b"
        plt.arrow(x,y,dx,dy,fc=col, ec=col, linewidth = 1, head_width=10000, head_length=8000)


plt.title('Wind Direction')
plt.show()