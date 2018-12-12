## Final_project.py
## Skeleton for  Final Project, Fall 2018
import requests
import json
from bs4 import BeautifulSoup
from secrets_finalproj import *
import plotly
import sqlite3
from tabulate import tabulate
import wikipedia
from datetime import datetime

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)
#----------------------
# Yelp Cache
#----------------------
CACHE_FNAME1 = 'yelp_data.json'
try:
    cache_file = open(CACHE_FNAME1, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION_1 = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION_1 = {}
#----------------------
# openweathermap Cache
#----------------------
CACHE_FNAME2 = 'Openweathermap_data.json'
try:
    cache_file = open(CACHE_FNAME2, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION_2 = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION_2 = {}
#==================
# GETTING YELP DATA
#===================
def yelp_make_request_using_cache(baseurl,params=None, headers=None):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION_1:
        print("Getting cached data...Yelp")
        return CACHE_DICTION_1[unique_ident]
    else:
        print("Making a request for new data...Yelp")
        resp = requests.get(baseurl, headers=headers, params=params)
        CACHE_DICTION_1[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION_1)
        fw = open(CACHE_FNAME1,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION_1[unique_ident]
#============================
# GETTING Openweathermap DATA
#============================
def OpenW_make_request_using_cache(baseurl,params=None,today_time=None):
    unique_ident = params_unique_combination(baseurl,params)
    unique_ident +=today_time
    if unique_ident in CACHE_DICTION_2:
        print("Getting cached data...Openweathermap")
        return CACHE_DICTION_2[unique_ident]
    else:
        print("Making a request for new data...Openweathermap")
        resp = requests.get(baseurl, params=params)
        CACHE_DICTION_2[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION_2)
        fw = open(CACHE_FNAME2,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION_2[unique_ident]

def get_city_restaurant(location, type, number):
    baseurl = "https://api.yelp.com/v3/businesses/search"
    params = {'location': location, 'limit':number, 'categories': type}
    headers={'Authorization': 'Bearer '+ yelp_api_key}
    contents = yelp_make_request_using_cache(baseurl, headers = headers, params=params)
    return contents

def get_city_weather(location):
    baseurl = 'https://api.openweathermap.org/data/2.5/weather?'
    params = {'appid':openweathermap_api_key,'q':location}
    contents = OpenW_make_request_using_cache(baseurl, params=params, today_time = str(datetime.now()).split()[0])
    return contents


def suggest_search(category):
    return wikipedia.search(category)


class Food_intro():
    def __init__(self, content, images):
        self.content = content
        self.images = images
    def __str__(self):
        return self.content+'\n\n\n'+'== Food images Link shown as follows ==' +'\n'+self.images

def get_details_food(food_type):
    food = wikipedia.page(food_type)
    content = food.content
    images=''
    for i in range(len(food.images)):
        images += food.images[i]
        images += '\n'
    food_intro = Food_intro(content, images)
    return food_intro



#===============
#init database
#===============

DBNAME = 'restaurant_info.db'
def init_db():
    conn=sqlite3.connect('restaurant_info.db')
    cur=conn.cursor()
    statement='''
        DROP TABLE IF EXISTS 'Restaurants' ;
    '''
    cur.execute(statement)
    statement='''
        DROP TABLE IF EXISTS 'Weather' ;
    '''
    cur.execute(statement)
    conn.commit()
    statement='''
        CREATE TABLE 'Restaurants' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT,
            'url' TEXT,
            'Ratings' REAL,
            'Price' TEXT,
            'latitude' TEXT,
            'longitude' TEXT,
            'streetAdress' TEXT,
            'city' TEXT,
            'state_name' TEXT,
            'locationZip_code' TEXT,
            'display_phone' TEXT,
            'category1' TEXT,
            'category2' TEXT,
            'category3' TEXT,
            'image_url' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()
    statement='''
        CREATE TABLE 'Weather' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT,
            'description' TEXT,
            'temp' REAL,
            'pressure' INT,
            'humidity' INT,
            'temp_min' REAL,
            'temp_max' REAL,
            'visibility' INT,
            'wind_speed' REAL,
            'date' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()



#================================================
# insert restaurant infornmation and weather data
#================================================

def insert_db():
    conn=sqlite3.connect('restaurant_info.db')
    cur=conn.cursor()
    restaurant_data = json.load(open(CACHE_FNAME1))
    for restaurant_li in restaurant_data.values():
            restaurant_li = list(restaurant_li.values())
            for each in restaurant_li[0]:
                try:
                    restaurant_insertion = (None, each['name'], each['url'],
                    each['rating'], each['price'], each['coordinates']['latitude'],
                    each['coordinates']['longitude'], each['location']['address1'],
                    each['location']['city'].upper(), each['location']['state'].upper(), each['location']['zip_code'],
                    each['display_phone'])

                except:
                    restaurant_insertion = (None, each['name'], each['url'],
                    each['rating'], 'No price available', each['coordinates']['latitude'],
                    each['coordinates']['longitude'],each['location']['address1'],
                    each['location']['city'].upper(),each['location']['state'].upper(), each['location']['zip_code'],
                    'No Phone Number')
                try:
                    restaurant_insertion += (each['categories'][0]['title'].upper(),)
                except:
                    restaurant_insertion += ('None type',)
                try:
                    restaurant_insertion += (each['categories'][1]['title'].upper(),)
                except:
                    restaurant_insertion += ('None type',)
                try:
                    restaurant_insertion += (each['categories'][2]['title'].upper(),)
                except:
                    restaurant_insertion += ('None type',)
                try:
                    restaurant_insertion += (each['image_url'],)
                except:
                    restaurant_insertion += ('No Image available',)

                restaurant_statement = 'INSERT INTO "Restaurants" '
                restaurant_statement += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '

                cur.execute(restaurant_statement, restaurant_insertion)
    conn.commit()

    weather_data = json.load(open(CACHE_FNAME2))
    weather = list(weather_data.values())
    for i in range(len(weather)):
        try:
            weather_insertion = (None, weather[i]['name'].upper(), weather[i]['weather'][0]['description'], weather[i]['main']['temp'],
            weather[i]['main']['pressure'], weather[i]['main']['humidity'], weather[i]['main']['temp_min'],
            weather[i]['main']['temp_max'], weather[i]['visibility'], weather[i]['wind']['speed'],str(datetime.now()).split()[0])
            weather_statement = 'INSERT INTO "Weather" '
            weather_statement += 'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '
        except:
            continue
        cur.execute(weather_statement, weather_insertion)
    conn.commit()
    conn.close()



#========================================================
# Plot Recommended Restaurant Locations in Plotly Offline
#========================================================

restaurant_lat_vals = []
restaurant_lon_vals = []
restaurant_text_vals = []

def restaurant_location_query(city,category):
    try:
        conn = sqlite3.connect('restaurant_info.db')
        cur = conn.cursor()
    except Error as e:
        print(e)
    city = city.split(',')

    if 'food' in category:
        query = '''
        SELECT  Name, category1, streetAdress, longitude, latitude, Price, Ratings, display_phone
        From Restaurants WHERE city='{}' and state_name='{}'
        '''.format(city[0].strip().upper(),city[1].strip().upper())
    else:
        query = '''
        SELECT  Name, category1, streetAdress, longitude, latitude, Price, Ratings, display_phone
        From Restaurants WHERE city='{}' and state_name='{}' and category1 = '{}'
        '''.format(city[0].strip().upper(),city[1].strip().upper(), category.upper())
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        text=''
        restaurant_lat_vals.append(row[4])
        restaurant_lon_vals.append(row[3])
        text = row[0]+'['+row[1]+']('+row[5]+'||'+str(row[6])+')-'+row[2]+'-'+row[7]
        restaurant_text_vals.append(text)
    conn.close()

def plot_restaurant_site_offline(city):
    try:
        min_lat = 10000
        max_lat = -10000
        min_lng = 10000
        max_lng = -10000

        lat_vals = restaurant_lat_vals
        lng_vals = restaurant_lon_vals
        for str_v in lat_vals:
            v = float(str_v)
            if v < min_lat:
                min_lat = v
            if v > max_lat:
                max_lat = v
        for str_v in lng_vals:
            v = float(str_v)
            if v < min_lng:
                min_lng = v
            if v > max_lng:
                max_lng = v

        max_range = max(abs(max_lat - min_lat), abs(max_lng - min_lng))
        padding = max_range * .10
        lat_axis = [min_lat - padding, max_lat + padding]
        lng_axis = [min_lng - padding, max_lng + padding]

        data = [ dict(
                type = 'scattermapbox',
                lon = lng_vals,
                lat = lat_vals,
                text = restaurant_text_vals,
                mode = 'markers',
                marker = dict(
                    size = 8,
                    symbol = 'restaurant',
                ))]
        center_lat = (max_lat+min_lat) / 2
        center_lng = (max_lng+min_lng) / 2
        layout = dict(
                title = 'Restaurants map for '+str(city),
                autosize=True,
                showlegend = False,
                hovermode = "closest",
                mapbox=dict(
                    accesstoken=MAPBOX_TOKEN,
                    bearing=0,
                    center=dict(
                        lat=center_lat,
                        lon=center_lng
                    ),
                    pitch=0,
                    zoom=10,
                ),
            )


        fig=dict(data=data, layout=layout )
        div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True)
        return div
    except ValueError:
        pass

#=================
# interactive Part
#=================

def weather_city(city):
    city = city.split(',')
    # try:
    conn = sqlite3.connect('restaurant_info.db')
    cur = conn.cursor()
    statement =" Select Name,description,temp,wind_speed From Weather WHERE name='{}' and date='{}' ".format(city[0].strip().upper(),str(datetime.now()).split()[0])
    print(statement)
    results=cur.execute(statement)
    results_list=results.fetchall()
    return results_list
    # except:
        # return 0


def get_full_info(city,category,number):
    global res_li
    try:
        conn = sqlite3.connect('restaurant_info.db')
        cur = conn.cursor()
        city = city.split(',')
        limit = ' LIMIT {} '.format(number)
        if 'food' in category:
            statement = '''
            SELECT Name, Ratings, Price, streetAdress,
            display_phone, category1, image_url
            From Restaurants WHERE city='{}' and state_name='{}'
            '''.format(city[0].strip().upper(),city[1].strip().upper())
        else:
            statement = '''
            SELECT Name, Ratings, Price, streetAdress,
            display_phone, category1, image_url
            From Restaurants WHERE city='{}' and state_name='{}' and category1 = '{}'
            '''.format(city[0].strip().upper(),city[1].strip().upper(), category.strip().upper())

        statement += limit
        results=cur.execute(statement)
        res_li =results.fetchall()
        conn.close()
        return res_li
    except:
        return 0


def get_all_res_info(sortby='Ratings', sortorder='desc'):
    global res_li
    if sortby == 'Ratings':
        sortcol = 1
    elif sortby == 'Price':
        sortcol = 2
    else:
        sortcol = 0

    rev = (sortorder == 'desc')
    sorted_list = sorted(res_li, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list
