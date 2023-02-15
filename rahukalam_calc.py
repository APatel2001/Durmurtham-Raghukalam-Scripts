import time
import requests
import ast
import datetime
import pytz
import pandas as pd
localtime = pytz.timezone('US/Pacific')

def get_rahukalam(year = None, month = None, day = None):
    #get the day of the week
    day_of_week = {}
    day_of_week[0] = "Monday"
    day_of_week[1] = "Tuesday"
    day_of_week[2] = "Wednesday"
    day_of_week[3] = "Thursday"
    day_of_week[4] = "Friday"
    day_of_week[5] = "Saturday"
    day_of_week[6] = "Sunday"

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
        if mydata["status"] == "INVALID_DATE":
            return "n"
        today = day_of_week[datetime.datetime(year, month, day).weekday()]
        mydate = datetime.datetime(year, month, day)
        mydate += datetime.timedelta(days=1)
        a = localtime.localize(mydate)
        is_dst = bool(a.dst())
    dict_str = dict_str = byte_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

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
    #calculate difference in time
    sunset_hours += 12
    if (sunset_minutes < sunrise_minuties):
        sunset_minutes += 60
        sunset_hours -= 1
    sunset_hours -= sunrise_hours
    sunset_minutes -= sunrise_minuties
    final_difference = (sunset_minutes / 60) + sunset_hours
    #calculate ahas
    ahas = final_difference / 8
    ahas_decimal = ahas
    ahas_hours = 0
    while ahas_decimal > 1:
        ahas_decimal -= 1
        ahas_hours +=1
    ahas_minutes_dec = 60 * ahas_decimal
    ahas_minutes = 0
    while ahas_minutes_dec > 1:
        ahas_minutes_dec-= 1
        ahas_minutes+=1
    if ahas_minutes_dec >= 0.5:
        ahas_minutes += 1

    #Rahukalam Calculations    
    Rahukalam = {}
    Rahukalam["Ignore"] = ""
    Rahukalam["Monday"] = ""
    Rahukalam["Saturday"] = ""
    Rahukalam["Friday"] = ""
    Rahukalam["Wednesday"] = ""
    Rahukalam["Thursday"] = ""
    Rahukalam["Tuesday"] = ""
    Rahukalam["Sunday"] = ""
    for key in Rahukalam:
        h = sunrise_hours
        m = sunrise_minuties
        sunrise_hours += ahas_hours
        sunrise_minuties += ahas_minutes
        if sunrise_minuties > 59:
            sunrise_hours += 1
            sunrise_minuties -= 60
        if key == 'Sunday':
            if sunrise_minuties < 10 and m >= 10:
                Rahukalam[key] = f'{h}:{m}-{sunrise_hours}:0{sunrise_minuties}'
            elif m < 10 and sunrise_minuties >= 10:
                Rahukalam[key] = f'{h}:0{m}-{sunrise_hours}:{sunrise_minuties}'
            elif m < 10 and sunrise_minuties < 10:
                Rahukalam[key] = f'{h}:0{m}-{sunrise_hours}:0{sunrise_minuties}'
            else:
                Rahukalam[key] = f'{h}:{m}-{sunrise_hours}:{sunrise_minuties}'





        if sunrise_minuties < 10 and m >= 10:
            Rahukalam[key] = f'{h}:{m}-{sunrise_hours}:0{sunrise_minuties}'
        elif m < 10 and sunrise_minuties >= 10:
            Rahukalam[key] = f'{h}:0{m}-{sunrise_hours}:{sunrise_minuties}'
        elif m < 10 and sunrise_minuties < 10:
            Rahukalam[key] = f'{h}:0{m}-{sunrise_hours}:0{sunrise_minuties}'
        else:
            Rahukalam[key] = f'{h}:{m}-{sunrise_hours}:{sunrise_minuties}'

    return(Rahukalam[today])
        

def convert_to_excel(yr):
    year = yr
    month = 1
    day = 1
    Date = []
    Rahukalam_arr = []
    id_arr = []
    counter = 1
    while month <= 12 and day < 33:
        printVal = get_rahukalam(year, month, day)
        if printVal == "n":
            month+=1
            day = 1
            continue
        print(f'{counter} {month}-{day}-{year}: {printVal}')
        Date.append(f'{month}-{day}-{year}')
        id_arr.append(counter)
        Rahukalam_arr.append(printVal)
        day+=1
        counter+=1

    df = pd.DataFrame({'ID': id_arr, 'Date': Date, 'Rahukalam': Rahukalam_arr})
    writer = pd.ExcelWriter(f'rahukalam_{yr}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Rahukalam', index=False)
    writer.save()
#convert_to_excel(2020)
#print('------------------')
#convert_to_excel(2021)


