#After told to do base on 0.5 radius
import pandas as pd
import geopandas as gpd
import numpy as np
import requests
import csv
import shapely
from geopandas import GeoSeries
from shapely.geometry import Point
from shapely.geometry import Polygon

def main():
    fileN = "transit_equity_team1\\programs\\tract_incomes_merged.csv"
    df = pd.read_csv(fileN)
    #print(df.head(5))
    #print(add_census_tract())
    #geometry_df = df['geometry']
    #print(geometry_df.head(5))
    #ls = geometry_df.values.tolist()
    #print(len(ls))
    #print(ls[0])
    #g = GeoSeries()
    #df = gpd.GeoDataFrame(df)
    #print(df.head(4))
    inpfile = csv.reader(open(fileN, 'r'))

    #santiize input ignoring the Polygon
    ct = 0
    ls = [] #santized polygon without the Polygon

    incomeLs = []
    for row in inpfile:
        ct += 1
        if (ct == 1):
            continue #ignore the first row\
        #if (ct == 4):
            #break
        #print(row[9][0]) #geodata
        #print(row[9][10:-2:])
        js = row[9][10:-2:]
        bs = js.split(',')
        ts = []
        #print(bs)
        #print(bs)
        #ls.append(bs)
        incomeLs.append(row[6])
        print(ct)
        if(ct == 5080):
            break #just to test polygon
        if (ct == 5080 or ct == 5081 or ct == 5082 or ct == 5083):
            continue #skip the multipolygon ones
        #if (ct == 5246 or ct == 5247 or ct == 5248):
            #print(row[0])
            #continue
        for ind in range(len(bs)):
            if (ind == 0):
                #print(bs[ind])
                sp = bs[ind].split(' ')
                kp = []
                for s in sp:
                    #st =  [int(i) for i in s.split() if i.isdigit()] 
                    #if (ct == 5246):
                        #kp.append(float(st[0:-1]))
                    #else:
                        #kp.append(float(s))
                    kp.append(float(s))
                #for s in range(len(sp)):
                    #st =  [int(i) for i in s.split() if i.isdigit()] 
                    #if (ct == 5246):
                        #kp.append(float(st[0:-1]))
                    #else:
                        #kp.append(float(s))
                        #if (ct >= 5246):
                            #if(s == 0):
                        #else:
                            #kp.append(float(sp[s]))
                #ts.append(p)
                ts.append(kp)
                #print(sp)
            else:
                sp = bs[ind].split(' ')
                sp = sp[1:]
                kp = []
                for s in sp:
                    #st = [int(i) for i in s.split() if i.isdigit()] 
                    #if (ct == 5246):
                        #kp.append(float(st[0:-1]))
                    #else:
                        #kp.append(float(s))
                    kp.append(float(s))
                #ts.append(p)
                ts.append(kp)
                #ts.append(sp)

                #print(sp)
            #cd = coord.split(' ')
            #print(cd)
        #print(ts)
        #print(ts)
        ls.append(ts) #append the list of polygon coords

    for t in ls:
        #append the to the polygon variable
        print(t)
        poly = Polygon(t)
        break
    return 0
main()