import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import math

from WeatherHourly import WeatherHourly


def getRainTotal(html):
    html = requests.get(html).text
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find_all('span', class_='wu-value wu-value-to')
    print(str(text) + str("  TEXT"))
    for i in text:
        print(i.text)
    toReturn = text[12].text
    return toReturn


def getWeatherLists(html_string):

    weatherLists = []

    table = pd.read_html(html_string)[4]

    hoursList = table.to_numpy()[2].flatten().tolist()

    hoursList = hoursList[1:]

    TempList = table.to_numpy()[3].flatten().tolist()

    TempList = TempList[1:]

    WindChillList = table.to_numpy()[5].flatten().tolist()

    WindChillList = WindChillList[1:]

    SurfaceWindList = table.to_numpy()[6].flatten().tolist()

    SurfaceWindList = SurfaceWindList[1:]

    GustList = table.to_numpy()[8].flatten().tolist()

    GustList = GustList[1:]

    SkyCoverList = table.to_numpy()[9].flatten().tolist()

    SkyCoverList = SkyCoverList[1:]

    PrecipitationPotentialList = table.to_numpy()[10].flatten().tolist()

    PrecipitationPotentialList = PrecipitationPotentialList[1:]

    RelativeHumidityList = table.to_numpy()[11].flatten().tolist()

    RelativeHumidityList = RelativeHumidityList[1:]

    rainList = table.to_numpy()[12].flatten().tolist()

    rainList = rainList[1:]

    thunderList = table.to_numpy()[13].flatten().tolist()
    thunderList = thunderList[1:]

    snowList = table.to_numpy()[14].flatten().tolist()
    snowList = snowList[1:]

    freezingRainList = table.to_numpy()[15].flatten().tolist()
    freezingRainList = freezingRainList[1:]

    sleetList = table.to_numpy()[16].flatten().tolist()
    sleetList = sleetList[1:]

    for e in range(24):
        hour = hoursList[e]
        if (hour[0:1] == '0'):
            hour = int(hour[1])
        else:
            hour = int(hour)
        temp = int(TempList[e])
        windChill = WindChillList[e]
        surfaceWind = SurfaceWindList[e]
        gust = GustList[e]
        skyCover = SkyCoverList[e]
        precipitation = PrecipitationPotentialList[e]
        humidity = RelativeHumidityList[e]
        rain = rainList[e]
        thunder = thunderList[e]
        snow = snowList[e]
        freezingRain = freezingRainList[e]
        sleet = sleetList[e]

        elementToBeAdded = WeatherHourly(hour, temp, windChill, surfaceWind, gust, skyCover, precipitation, rain, humidity, thunder, snow, freezingRain, sleet)

        weatherLists.append(elementToBeAdded)


    return weatherLists

def getSunsetRise(html_string):
    list = []
    html = requests.get(html_string).text
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find('p', class_ = 'dn-mob').text
    list.append(text[0:5])    # Index 1 list is the sunrise
    list.append(text[10:15])  # Index 2 list is the sunset
    return list

def makeTodaysObjectList(list):
    todayWeatherList = []

    checker = False

    for o in list:
        if (o.hour >= 0 and not (checker)):
            if (o.hour == 23):
                checker = True
            todayWeatherList.append(o)
    return todayWeatherList

def getNightList(htmlsun, htmlweather):
    sunList = getSunsetRise(htmlsun)
    sunset = sunList[1]
    nightStartHour = 0

    if (int(sunset[2]) < 3):
        nightStartHour = int(sunset[0])
    else:
        nightStartHour = int(sunset[0]) + 1

    nightStartHour = nightStartHour + 12

    weatherTextList = getWeatherLists(htmlweather)

    weatherObjList = makeTodaysObjectList(weatherTextList)


    nightList = []

    for i in weatherObjList:
        if (int(i.hour) >= nightStartHour):
            nightList.append(i)

    return nightList


def getDayList(htmlsun, htmlweather):

    sunList = getSunsetRise(htmlsun)

    sunset = sunList[1]

    nightStartHour = 0

    if (int(sunset[2]) < 3):
        nightStartHour = int(sunset[0])
    else:
        nightStartHour = int(sunset[0:1]) + 1

    nightStartHour = nightStartHour + 12

    weatherTextList = getWeatherLists(htmlweather)

    weatherObjList = makeTodaysObjectList(weatherTextList)

    dayList = []

    for i in weatherObjList:
        if (int(i.hour) < nightStartHour):
            dayList.append(i)

    return dayList



def isRainy(list):
    fiftyPercentCounter = 0
    for i in list:
        if (int(i.precipitation) > 50):
            fiftyPercentCounter += 1

    if (fiftyPercentCounter > 0 ):
        return True
    else:
        return False

def isSleet(list):
    sleetCounter = 0
    for i in list:
        if (i.sleet == 'Lkly' or i.sleet == 'Ocnl'):
            sleetCounter += 1

    if (sleetCounter > 0):
        return True
    else:
        return False


def isWindy(list):


    windyCounter = 0
    for i in list:
        if (not math.isnan(float(i.gust))):
            if int(i.surfaceWind) > 14:
                windyCounter += 1
            if int(i.gust) > 19:
                windyCounter += 1
    if windyCounter > 2:
        return True
    else:
        return False


def isSnowy(list):
    snowyCounter = 0
    for i in list:
        if (i.snow == 'Lkly' or i.snow == 'Ocnl'):
            snowyCounter += 1

    if (snowyCounter > 0):
        return True
    else:
        return False

def isFreezingRain(list):
    fRainCounter = 0
    for i in list:
        if (i.freezingRain == 'Lkly' or i.freezingRain == 'Ocnl'):
            fRainCounter += 1

    if (fRainCounter > 0):
        return True
    else:
        return False

def isStormy(list):

    stormyCounter = 0
    for i in list:
        if (i.thunder == 'Lkly' or i.thunder == 'Ocnl'):
            stormyCounter += 1

    if (stormyCounter > 0):
        return True
    else:
        return False

def isCloudy(list):
    cloudTotal = 0.0
    for i in list:
       cloudTotal += float(i.skyCover)

    averageCloudCover = cloudTotal / len(list)
    if (averageCloudCover > 62.5):
        return True
    else:
        return False

def isPartlyCloudy(list):
    cloudTotal = 0.0
    for i in list:
        cloudTotal += float(i.skyCover)

    averageCloudCover = cloudTotal / len(list)
    if (averageCloudCover <= 62.5 and averageCloudCover >= 37.5):
        return True
    else:
        return False

def isClear(list):
    cloudTotal = 0.0
    for i in list:
        cloudTotal += float(i.skyCover)

    averageCloudCover = cloudTotal / len(list)
    if (averageCloudCover < 37.5):
        return True
    else:
        return False

def maxGust(list):
    max = 0
    for i in list:
        if (not math.isnan(float(i.gust))):
            if (int(i.gust) > max):
                max = int(i.gust)
    return max

def getHigh(list):
    high = 0
    for i in list:
        if (int(i.temp) > high):
            high = i.temp
    return high

def getLow(list):
    low = 200
    for i in list:
        if (int(i.temp) < low):
            low = i.temp
    return low

def getRealHigh(list):
    rHigh = 0    
    for i in list:
        if (not pd.isnull(i.windChill)):
             if (int(i.windChill) > int(rHigh)):
                rHigh = i.windChill
        else:
            return None
    return rHigh

def getRealLow(list):
    rLow = 200
    for i in list:
        if (not pd.isnull(i.windChill)):
            if (int(i.windChill) < int(rLow)):
                rLow = i.windChill
        else:
            return None
    return rLow

def getRealTempCurrent(list):
    if (not pd.isnull(list[0].windChill)):
        return list[0].windChill
    else:
        return list[0].temp


def getRelativeHumidity(list):
    humidityTotal = 0.0
    for i in list:
        humidityTotal = + float(i.humidity)

    averageHumidity = humidityTotal / len(list)

    return averageHumidity

def getAverageWind(list):
    surfaceWindTotal = 0.0
    for i in list:
        surfaceWindTotal += float(i.surfaceWind)

    averageSurfacewind = surfaceWindTotal / len(list)

    return int(averageSurfacewind)


#if __name__ == '__main__':
    #tableDebug = pd.read_html('https://forecast.weather.gov/MapClick.php?lat=42.6879&lon=-89.0182&lg=english&&FcstType=digital')[4]
    
    #print(tableDebug.iloc[2])
    
    #print(getSunsetRise('https://www.timeanddate.com/sun/usa/janesville'))
    
    #getWeatherLists('https://forecast.weather.gov/MapClick.php?lat=42.6813&lon=-89.0269&lg=english&&FcstType=digital')
    #print(getDayList('https://www.timeanddate.com/sun/usa/janesville','https://forecast.weather.gov/MapClick.php?lat=42.6813&lon=-89.0269&lg=english&&FcstType=digital')[0].hour)
        
        























