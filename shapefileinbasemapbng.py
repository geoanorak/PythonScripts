# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 20:09:59 2015

@author: npmj
"""
import fiona
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pyproj
from matplotlib.patches import Polygon
import numpy as np


def randomcolour():
    r = np.random.uniform(0, 1)
    g = np.random.uniform(0, 1)
    b = np.random.uniform(0, 1)
    return (r, g, b)

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'i' means use intermediate resolution coastlines.
# lon_0, lat_0 are the central longitude and latitude of the projection.
m = Basemap(llcrnrlon=-10.5,llcrnrlat=49.5,urcrnrlon=3.5,urcrnrlat=59.5,
            resolution='i',projection='tmerc',lon_0=-4.36,lat_0=54.7)
# can get the identical map this way (by specifying width and
# height instead of lat/lon corners)
#m = Basemap(width=894887,height=1116766,\
#            resolution='i',projection='tmerc',lon_0=-4.36,lat_0=54.7)
m.drawcoastlines()
m.fillcontinents(color='pink',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-40,61.,2.))
m.drawmeridians(np.arange(-20.,21.,2.))
m.drawmapboundary(fill_color='aqua')
#lon = -1.5
#lat = 55
#USE PYPROJ to convert point from BNG to Lat/Lon
bng=pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')
lon,lat = pyproj.transform(bng,wgs84,424000,565000)
x,y = m(lon, lat)
m.plot(x,y, 'ro', markersize=6)
plt.title("Transverse Mercator Projection")
#m.readshapefile('c:/phil/dropbox/code/mapdata/London_congestion_43262', 'lc', drawbounds = False)
#m.readshapefile('c:/phil/dropbox/code/mapdata/London_congestion_charge', 'lc', drawbounds = False)
shplist =[]
shplist.append(fiona.open('c:/phil/dropbox/code/mapdata/London_congestion_charge.shp', 'r'))
shplist.append(fiona.open('c:/phil/dropbox/code/mapdata/London_a_roads.shp', 'r'))
shplist.append(fiona.open('c:/phil/dropbox/code/mapdata/metro.shp', 'r'))
shplist.append(fiona.open('c:/phil/dropbox/code/mapdata/London_boroughs.shp', 'r'))
shplist.append(fiona.open('c:/phil/dropbox/code/mapdata/ukcounty2.shp', 'r'))

for shpfile in shplist:
    for geom in shpfile:
        #get the geom
        #print geom['geometry']['type']
        xy = geom['geometry']['coordinates']
        datum = shpfile.crs.get('datum', 'none')
        if geom['geometry']['type']=='Point':
            #do something
            #print xy
            x = xy[0]
            y = xy[1]
            if datum == 'OSGB36':
                x1, y1 = pyproj.transform(bng,wgs84,x,y)
            else:
                x1, y1 = x, y
            x1, y1 = m(x1, y1)
            m.plot(x1, y1, 'bo')
        elif geom['geometry']['type']=='Polygon':
            #print 'Polygon'
            xy = geom['geometry']['coordinates'][0]
            x, y = zip(*xy) 
            if datum == 'OSGB36':
                x1, y1 = pyproj.transform(bng,wgs84,x,y)
                x1, y1 = m(x1, y1)
            else:
                x1, y1 = m(x, y)
            #Turn back into tuple to make patch object
            try:
                xy = zip(x1, y1)
                poly = Polygon(xy, facecolor=randomcolour(), alpha=0.4)
                plt.gca().add_patch(poly)
            except Exception as e:
                print e
            #m.plot(x1, y1, marker=None,color='b')
        elif geom['geometry']['type']=='MultiPolygon':
            print 'Polygon'
            xy = geom['geometry']['coordinates'][0][0]
            x, y = zip(*xy) 
            if datum == 'OSGB36':
                x1, y1 = pyproj.transform(bng,wgs84,x,y)
                x1, y1 = m(x1, y1)
            else:
                x1, y1 = m(x, y)
            #Turn back into tuple to make patch object
            try:
                xy = zip(x1, y1)
                poly = Polygon(xy, facecolor=randomcolour(), alpha=0.4)
                plt.gca().add_patch(poly)
            except Exception as e:
                print e
        else:
            x, y = zip(*xy) 
            #transform the geom to wgs84
            if datum == 'OSGB36':
                x1, y1 = pyproj.transform(bng,wgs84,x,y)
                x1, y1 = m(x1, y1)
            else:
                x1, y1 = m(x, y)
            #x1 = list(x1)
            #y1 = list(y1)
            #print x1, y1
            m.plot(x1, y1, marker=None,color=randomcolour(), linewidth=2.0)
    
#plt.legend()
plt.show()