from durmuhurtham import getDurmuhurtham1, getDurmuhurtham2, getSunrise, getSunset, getSunsetOrig
from rahukalam_calc import get_rahukalam
import pandas as pd

def convert_to_excel(yr):
    year = yr
    month = 1
    day = 1
    Date = []
    Rahukalam_arr = []
    Durmuhurtham1_arr = []
    Durmuhurtham2_arr = []
    sunrise_arr = []
    sunset_arr = []
    id_arr = []
    counter = 1
    while month <= 12 and day < 33:
        printVal1 = get_rahukalam(year, month, day)

        if printVal1 == "n":
            month+=1
            day = 1
            continue
        raghukalam2 = get_rahukalam(year, month, day)
        times = raghukalam2.split('-')
        times[1], today = getSunsetOrig(year, month, day)
        raghukalam2 = '-'.join(times)
        if (today == "Sunday"):
            printVal1 = raghukalam2
        printVal2 = getDurmuhurtham1(year, month, day)
        printVal3 = getDurmuhurtham2(year, month, day)
        printVal4 = getSunrise(year, month, day)
        printVal5 = getSunset(year, month, day)
        print(f'{counter} {month}-{day}-{year}: {printVal1} --------- {printVal2} --------- {printVal3} --------- {printVal4} --------- {printVal5}')
        Date.append(f'{month}-{day}-{year}')
        id_arr.append(counter)
        Rahukalam_arr.append(printVal1)
        Durmuhurtham1_arr.append(printVal2)
        Durmuhurtham2_arr.append(printVal3)
        sunrise_arr.append(printVal4)
        sunset_arr.append(printVal5)
        day+=1
        counter+=1

    df = pd.DataFrame({'ID': id_arr, 'Date': Date, 'Sunrise': sunrise_arr, 'Sunset': sunset_arr, 'Rahukalam': Rahukalam_arr, 'Durmuhurtham 1': Durmuhurtham1_arr, 'Durmuhurtham 2': Durmuhurtham2_arr})
    writer = pd.ExcelWriter(f'calculations_{yr}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Rahukalam', index=False)
    writer.save()

#function call, specify year you want calculations for
convert_to_excel(2023)

