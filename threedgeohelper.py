'''
Create Surfaces and TINS from attributes

This tool is designed to automate the process of creating TIN based stratigraphic multipatches from borehole or other data.

This tool splits a Shapefile or Feature Class based on attribute names selected by the user. It then creates an interpolated surface using the specified depth field (optionally it can turn the zvalue field into negative values ie. subsurface measurements).

The tool outputs a number of intermediate outputs which can be retained if necessary.

'''

# Creates multiple tifs and TINS suitable for generating MULTIPATCHES for 3D visualisation
# Data input assumes geology layers are as points with heights / depths of each stratigraphic layer as an attribute eg.
# FID, X, Y, strat1, strat2, strat3, strat4...
# 1,   -1.5, 56.9, -1234, -876, -456, -234...

# Add the fields you want to create TINS for in the tool - iterate over them generating surfaces and 3D TINs

# values can be inverted if depths are positives
# Once complete you can interpolate multipatches between the different 3D TINS to generate 3D block or fence diagrams

import arcgisscripting
import arcpy
from arcpy import env  
from arcpy.sa import *

#GET PARAMETERS
outWorkspace   = arcpy.GetParameterAsText(0)	#output workspace to store files
featureClass  = arcpy.GetParameterAsText(1)   	#input featureclass
zfield = arcpy.GetParameterAsText(2)			#the z fields in the input feature class that you want to create TINS / Surfaces for
invertvals = arcpy.GetParameterAsText(3)		#boolean to invert the depth / height values
cellsize = arcpy.GetParameterAsText(4)			#set cellsize of outputs

arcpy.env.cellSize = cellsize

gp = arcgisscripting.create()
gp.OverWriteOutput = 1
zfield = zfield.split(';')
#gp.AddMessage(zfield) 
env.workspace = outWorkspace

if invertvals =='true':
    invertvals = True
else:
    invertvals = False    

# Starts Geoprocessing

inputFile = featureClass
outDir = outWorkspace + "\\"

# Output a surface for each attribute
for each_attribute in zfield:
    if len(each_attribute) >= 1: 
        #Clean up field names to remove spaces and comma otherwise it crashes
        fnameeach_attribute = each_attribute.replace(' ', '')
        fnameeach_attribute = fnameeach_attribute.replace(',', '')
        env.cellSize = cellsize
        idw = arcpy.Idw_3d(featureClass, each_attribute, env.workspace + "\\" + fnameeach_attribute + ".tif", )
        gp.AddMessage(env.workspace + "/" + fnameeach_attribute + ".tif")           
        addtext = ''
        #INVERT THE RASTERS IF REQUIRED
        if invertvals:
            addRas = arcpy.Raster(env.workspace + "/" + fnameeach_attribute + ".tif")
            newRas = addRas * -1
            newRas.save(env.workspace + "/" + "inverse" + fnameeach_attribute + ".tif")
            addtext = 'inverse'
            
        #CREATE TINS
        dataset = featureClass
        spatialRef = arcpy.Describe(dataset).spatialReference
        tinstr = featureClass + " " + each_attribute + " masspoints"
        tin = arcpy.CreateTin_3d (addtext + fnameeach_attribute, spatialRef, tinstr)

        
del gp

#END	
