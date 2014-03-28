# -*- coding: utf-8 -*-
"""

@author: Phil James
reads data from postgres table with x, y and value (change as appropriate)
Converts to R data grid
Runs IDW tool in R and saves output
"""

import psycopg2
import rpy2.robjects as ro

#GET TABLE OF DATA FROM POSTGIS
def getdatatable(host, db, user, pword, sql):
    connstr = "host=" + host + " dbname=" + db + " user=" + user + " password=" + pword + " port=5433"
    print connstr
    conn = psycopg2.connect(connstr)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

#CONVERT TO R DATA GRID
def converttabletogrid(list, data, robjname):
    R = ro.r
    columns=zip(*data) #turns rows to columns
    columns=[ro.FloatVector(col) for col in columns]
    dataf = R['data.frame'](**dict(zip(list, columns)))
    #print dataf;
    ro.globalEnv[robjname]=dataf

#CREATE THE IDW
def createidw(robjname):
    R = ro.r    
    R.library('gstat')          #load libraries
    R.library('raster')         
    rstr = "data <- " + robjname + ""
    R(rstr)     
    R("coordinates(data) <- ~x+y")
    R("x.range <- as.integer(range(data@coords[,1]))")  #create ranges
    R("y.range <- as.integer(range(data@coords[,2]))") 
    #create a grid
    R("grd <- expand.grid(x=seq(from=x.range[1], to=x.range[2], by=100), y=seq(from=y.range[1], to=y.range[2], by=100))")
    R("coordinates(grd) <- ~x+y")
    #create IDW
    R("idw.out <- idw(value~1, data, grd, idp=2.5)")
    #plot it
    spplottext = "spplot(idw.out, \"var1.pred\", col.regions=topo.colors(20), pretty=TRUE, scales=list(draw=TRUE))"
    res = R(spplottext)
    savetojpg(spplottext)
    return res

def savetojpg(plottext):
    R = ro.r
    R("jpeg(\"c:/temp/lhidw.jpg\")")
    res = R(plottext)
    print(res)
    R("dev.off()")

#MAIN SCRIPT
#CHANGE SELECT STATEMENT AS NEEDED
data = getdatatable("localhost", "DBNAME", "postgres", "***", "SELECT as_test, \"Easting\", \"Northing\" FROM \"AS_GBASE\"")
#print data
list = ["value", "x", "y"]
converttabletogrid(list, data, 'ptslist')    
print ro.globalEnv['ptslist']
res = createidw('ptslist')
print res

