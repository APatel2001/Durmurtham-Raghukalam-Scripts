import time
from typing_extensions import final
import requests
import ast
import datetime
import pytz
import pandas as pd
localtime = pytz.timezone('US/Pacific')

def convTimeNum(mydata, is_dst, today):
    #Get Sunrise and Sunset Timings:
    sunrise = mydata['results']['sunrise']
    sunset = mydata['results']['sunset']
    sunrise_time = sunrise.split(" ")[0]
    sunset_time = sunset.split(" ")[0]
    sunrise_am_pm = sunrise.split(" ")[1]
    sunset_am_pm = sunset.split(" ")[1]
    #extract times
    sunrise_hours, sunrise_minuties, sunrise_seconds = map(int, sunrise_time.split(":"))
    sunset_hours, sunset_minutes, sunset_seconds = map(int, sunset_time.split(":"))
    orig_sunset_hours = sunset_hours
    orig_sunset_minutes = sunset_minutes
    #adjust time
    if sunrise_seconds >= 30:
        sunrise_minuties += 1
    if sunset_seconds >= 30:
        sunset_minutes += 1
    if (sunrise_minuties > 59):
        sunrise_hours+=1
        sunrise_minuties-=60
    if (sunset_minutes > 59):
        sunset_hours+=1
        sunset_minutes -= 60
    #convert to PST
    sunrise_hours += 16
    sunset_hours += 16
    while sunrise_hours > 12:
        sunrise_hours-=12
    while sunset_hours > 12:
        sunset_hours-=12
    if is_dst == True:
        sunrise_hours += 1
        sunset_hours += 1
    sunrise_am_pm = "AM"
    sunset_am_pm = "PM"
    
    return (sunrise_hours, 
            sunrise_minuties, 
            sunrise_am_pm, 
            sunset_hours, 
            sunset_minutes, 
            sunset_am_pm, 
            today,
            is_dst,
            orig_sunset_hours,
            orig_sunset_minutes)


def getSunriseSunset(year = None, month = None, day = None):
    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    byte_str = b''
    today = 0
    is_dst = False
    if year == None and month == None and day == None:
        byte_str = requests.get('https://api.sunrise-sunset.org/json?lat=37.7790262&lng=-122.419906').content
        today = day_of_week[datetime.datetime.today().weekday()]
        mydate = datetime.datetime.today()
        a = localtime.localize(mydate)
        is_dst = bool(a.dst())
    else:
        byte_str = requests.get(f'https://api.sunrise-sunset.org/json?lat=37.7790262&lng=-122.419906&date={year}-{month}-{day}').content
        dict_str = dict_str = byte_str.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        
        today = day_of_week[datetime.datetime(year, month, day).weekday()]
        mydate = datetime.datetime(year, month, day)
        mydate += datetime.timedelta(days=1)
        a = localtime.localize(mydate)
        is_dst = bool(a.dst())
    dict_str = dict_str = byte_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    return convTimeNum(mydata, is_dst, today)


def getDifference(sunrise_hours, sunrise_minuties, sunset_hours, sunset_minutes):
    #calculate difference in time
    sunset_hours += 12
    if (sunset_minutes < sunrise_minuties):
        sunset_minutes += 60
        sunset_hours -= 1
    sunset_hours -= sunrise_hours
    sunset_minutes -= sunrise_minuties
    final_difference = (sunset_minutes / 60) + sunset_hours
    return final_difference

def conv_min_hours(min):
    hours = min/60
    new_min = hours
    hours = 0
    while new_min > 1:
        new_min-=1
        hours+=1
    min_dec = new_min*60
    min_whole = 0
    while min_dec > 1:
        min_dec-=1
        min_whole+=1
    if min_dec >= 0.5:
        min_whole+=1
    return (hours, min_whole)

def durmuhurtham(sunrise_hours, sunrise_minuties, sunset_hours, sunset_minutes, durmuhurtham_num, today):
    final_difference = getDifference(sunrise_hours, sunrise_minuties, sunset_hours, sunset_minutes)
    div_15 = final_difference/15
    conv_minutes = div_15 * 60
    durm_mult = durmuhurtham_num[today] - 1
    durm = conv_minutes * durm_mult
    durm_hours1, durm_minutes1 = conv_min_hours(durm)
    durm_start_hours = sunrise_hours+durm_hours1
    durm_start_minutes = sunrise_minuties+durm_minutes1
    if durm_start_minutes > 59:
        durm_start_hours+=1
        durm_start_minutes-=60
    durm_hours2, durm_minutes2 = conv_min_hours(conv_minutes)
    durm_end_hours = durm_start_hours + durm_hours2
    durm_end_minutes = durm_start_minutes + durm_minutes2
    if durm_end_minutes > 59:
        durm_end_minutes-=60
        durm_end_hours+=1
    
    if (durm_start_minutes < 10) and (durm_end_minutes >= 10):
        return f'{durm_start_hours}:0{durm_start_minutes}-{durm_end_hours}:{durm_end_minutes}'
    elif (durm_start_minutes >= 10) and (durm_end_minutes < 10):
        return f'{durm_start_hours}:{durm_start_minutes}-{durm_end_hours}:0{durm_end_minutes}'
    elif (durm_start_minutes < 10) and (durm_end_minutes < 10):
        return f'{durm_start_hours}:0{durm_start_minutes}-{durm_end_hours}:0{durm_end_minutes}'
    return f'{durm_start_hours}:{durm_start_minutes}-{durm_end_hours}:{durm_end_minutes}'
    

def getSunrise(year = None, month = None, day = None):
    sunrise_hours, sunrise_minuties, sunrise_am_pm, sunset_hours, sunset_minutes, sunset_am_pm, today, is_dst, orig_sunset_hours, orig_sunset_minutes  = getSunriseSunset(year, month, day)
    if (sunrise_minuties < 10):
        return f'{sunrise_hours}:0{sunrise_minuties} {sunrise_am_pm}' 
    return f'{sunrise_hours}:{sunrise_minuties} {sunrise_am_pm}' 

def getSunset(year = None, month = None, day = None):
    sunrise_hours, sunrise_minuties, sunrise_am_pm, sunset_hours, sunset_minutes, sunset_am_pm, today, is_dst, orig_sunset_hours, orig_sunset_minutes = getSunriseSunset(year, month, day)
    if (sunset_minutes < 10):
        return f'{sunset_hours}:0{sunset_minutes} {sunset_am_pm}'
    return f'{sunset_hours}:{sunset_minutes} {sunset_am_pm}'

def getSunsetOrig(year = None, month = None, day = None):
    sunrise_hours, sunrise_minuties, sunrise_am_pm, sunset_hours, sunset_minutes, sunset_am_pm, today, is_dst, orig_sunset_hours, orig_sunset_minutes = getSunriseSunset(year, month, day)
    if (orig_sunset_minutes < 10):
        return (f'{orig_sunset_hours}:0{orig_sunset_minutes}', today)
    return (f'{orig_sunset_hours}:{orig_sunset_minutes}', today)

def getDurmuhurtham1(year = None, month = None, day = None):
    durmuhurtham1 = {"Sunday": 14, "Monday": 9, "Tuesday": 4, "Wednesday": 8, "Thursday": 6, "Friday": 4, "Saturday": 1}
    sunrise_hours, sunrise_minuties, sunrise_am_pm, sunset_hours, sunset_minutes, sunset_am_pm, today, is_dst, orig_sunset_hours, orig_sunset_minutes = getSunriseSunset(year, month, day)
    return durmuhurtham(sunrise_hours, sunrise_minuties, sunset_hours, sunset_minutes, durmuhurtham1, today)
def getDurmuhurtham2(year = None, month = None, day = None):
    durmuhurtham2 = {"Sunday": -1, "Monday": 12, "Tuesday": 7, "Wednesday": -1, "Thursday": 12, "Friday": 9, "Saturday": 2}
    sunrise_hours, sunrise_minuties, sunrise_am_pm, sunset_hours, sunset_minutes, sunset_am_pm, today, is_dst, orig_sunset_hours, orig_sunset_minutes = getSunriseSunset(year, month, day)
    if today != "Sunday" and today != "Wednesday" and today != "Tuesday":
        return durmuhurtham(sunrise_hours, sunrise_minuties, sunset_hours, sunset_minutes, durmuhurtham2, today)
    elif today == "Sunday" or today == "Wednesday":
        return None
    elif today == "Tuesday":
        today_date = str(datetime.datetime.today().date() + datetime.timedelta(days=1))
        today_year = int(today_date[0:4])
        today_month = int(today_date[5:7])
        today_day = int(today_date[8:10])
        sunrise_hours2, sunrise_minuties2, sunrise_am_pm2, sunset_hours2, sunset_minutes2, sunset_am_pm2, today2, is_dst2, orig_sunset_hours, orig_sunset_minutes = getSunriseSunset(today_year, today_month, today_day)
        return durmuhurtham(sunset_hours, sunset_minutes, sunrise_hours2, sunrise_minuties2, durmuhurtham2, today)
    


