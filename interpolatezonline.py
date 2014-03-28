# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 12:21:37 2014

@author: npmj
"""


import psycopg2

#def getdatatable(host, db, user, pword, sql):
connstr = "host=" + "localhost" + " dbname=" + "npmjtest" + " user=" + "ceguser" + " password=" + "***" + " port=5433"
print connstr
conn = psycopg2.connect(connstr)
cursor = conn.cursor()
sql = "SELECT ST_ASTEXT(geom) FROM line3d_2"
cursor.execute(sql)
data = cursor.fetchall()

f = open('c:/temp/dataout.txt', 'w')
for r in data:
    #print r
    for i in range(1, 10):
        res = float(i) / 10
        cursor.execute("SELECT ST_AsEWKT(ST_Line_Interpolate_Point(ST_GeomFromText(%s), %s))", (data[0],res))

        data2 = cursor.fetchall()
        print data2
        f.write(str(data2))
        f.write("\n")
    
cursor.close()
conn.close()
f.close()