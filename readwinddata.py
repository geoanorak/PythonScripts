# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:10:02 2015

@author: Phil James @geoanorak
Plot wind directions using Basemap
Data from met office data.gov.uk http://data.gov.uk/metoffice-data-archive
Observations
Can also use api to get the data
Here data in CSV format

DATA FORMAT IS:
['Site Code', 'Site Name', 'Latitude', 'Longitude', 'Region', 'Observation Time', 'Observation Date', 'Wind Direction', 'Wind Speed', 'Wind Gust', 'Visibility', 'Screen Temperature', 'Pressure', 'Pressure Tendency', ' Significant Weather']
['3008', 'FAIR ISLE (3008)', '59.53', '-1.63', 'Orkney & Shetland', '12:00', '25/02/2015', 'SW', '14', '', '25000', '6.3', '1006', '#', 'Sunny intervals']
"""

import csv
import pylab as plt
from mpl_toolkits.basemap import Basemap
import math

data = []

#READ THE CSV FILE AND EXTRACT DATA
with open('c:/phil/dropbox/code/mapdata/wind.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        data.append(row)

flip = zip(*data)
lat = list(flip[2])
lon = list(flip[3])
wdir = list(flip[7])
wspeed = list(flip[8])

#CALCULATE THE WIND DIRECTION

#set up the list of compass rose points
dirs=['N','NNE', 'NE', 'ENE','E', 'ESE', 'SE','SSE','S', 'SSW', 'SW', 'WSW','W', 'WNW', 'NW', 'NNW']
#set up bearings
angs = range(0,720, 45)
for i in range(0, len(angs)):
    angs[i] = float(angs[i]) / 2

#lookup compass direction and get bearing - create dictionary
dirdict = dict(zip(dirs, angs))

#flips the directions by 180 (as wind is direction FROM not TO but arrows are direction TO)
windangs = ['caption']
for i in range(1, len(lat)):
    try:
        val = dirdict[wdir[i]]
        val = val + 180
        if val>=360:
            val = val - 360
        windangs.append(val)
    except :
        windangs.append(0.0)
    #print lat[i], lon[i], wdir[i], wspeed[i], windangs[i]
    
#PLOTTING STUFF
#get rid of headings
lon.pop(0)
lat.pop(0)
windangs.pop(0)
wspeed.pop(0)

#convert strings to floats
lon2 = map(float, lon)
lat2 = map(float, lat)
windangs2 = map(float, windangs)
wspeed2 = map(float, wspeed)

#create basemap with EPSG:27700
m = Basemap(llcrnrlon=-10.5,llcrnrlat=49.5,urcrnrlon=3.5,urcrnrlat=59.5,resolution='i',projection='tmerc',lon_0=-4.36,lat_0=54.7)
m.drawcoastlines()

#Plot the arrows on the map
for i in range(0, len(lon2)):
    x,y = m(lon2[i], lat2[i])
    rad = math.radians(windangs2[i])
    dx =20000 * math.sin(rad)
    dy = 20000 * math.cos(rad)
    plt.arrow(x,y,dx,dy,fc="b", ec="b", linewidth = 1, head_width=10000, head_length=8000)


plt.title('Wind Direction')
plt.show()