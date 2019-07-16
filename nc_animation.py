#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:45:44 2019

@author: colby
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# plt.ioff()

geo = gpd.read_file("NC_VTD/NC_VTD.shp")

fis_to_vtd = dict()

with open("arcgis_FIDtovtdkeymap.txt") as f:
    # Discard the first line; it's just column headers
    f.readline()
    
    for line in f:
        fis_to_vtd[int(line.split()[0])] = line.split()[1]
        
maps = ["districtMap%05d" % i for i in range(0,24517)]

i = 0
for m in maps:
    i += 1
    if (i % 10 == 0): print(i)
    assignments = []
    for line in open("./districtMaps/" + m + ".txt"):
        fis = int(line.split()[0]) + 1
        assignments.append((fis_to_vtd[fis], int(line.split()[1])))
    
    df = pd.DataFrame(assignments, columns=['VTD', 'district'])
    
    geo1 = pd.merge(geo, df, on = ["VTD", "VTD"])
    
    geo1.plot(column='district', cmap='nipy_spectral', figsize=(8,6))
    
    plt.axis('off')
    plt.savefig('/tmp/plots/' + m + '.png')
    plt.close()

