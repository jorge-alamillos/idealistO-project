from dotenv import load_dotenv
import requests
load_dotenv()
import os
import geopandas as gpd
import pandas as pd
import fiona

def get_coordinates(address):
    key = os.getenv('GOOGLEAUTH')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    rqst  = requests.get(url + address + '&key=' + key)    
    datos = rqst.json()
    location = datos['results'][0]['geometry']['location']
    print(url + address + '&key=' + key)
    return location

def coordintes2gdf(x):
    geo = gpd.GeoDataFrame({'lat': [x["lat"]], 'lng': [x["lng"]]})
    gdf = gpd.GeoDataFrame(geo, geometry=gpd.points_from_xy(geo.lng, geo.lat),crs="EPSG:4326")
    return gdf.to_crs("EPSG:4326")

def read_barrios():
    barrios = gpd.read_file("BARRIOS.shp")
    return barrios.to_crs("EPSG:4326")

def get_barrio(coord,barrios):
    return gpd.sjoin(coord, barrios, how="left", op='within')   

def read_barr_punt():
    return pd.read_csv("barrios_puntuaciones.csv")
    
    
def get_punt(barrio,barr_punt):
    distrito = barrio["NOMBRE"].to_string(index=False).lstrip()
    x = barr_punt[barr_punt["NOMBRE"]==distrito]
    security = int(x["security"].to_string(index=False).lstrip())
    transport = int(x["transport"].to_string(index=False).lstrip())
    health = int(x["health"].to_string(index=False).lstrip())
    education = int(x["education"].to_string(index=False).lstrip())
    return security,transport,health,education
     
