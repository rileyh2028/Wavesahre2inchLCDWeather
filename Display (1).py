import time

from datetime import date

from PIL import Image, ImageDraw, ImageFont

import WeatherData

from WaveshareModule import LCD_2inch

def getDayImage(list):
    photoFileDay = ''

    # if len(dayList) == 0:
        # canvas.create_text(172, 130, text="(It is Night)", fill="black", font=('Terminal'), anchor=CENTER)
        # canvas.pack()
    if WeatherData.isStormy(list):
        photoFileDay = 'stormy.png'
    elif WeatherData.isRainy(list):  ########
        if (WeatherData.isSnowy(list)):
            photoFileDay = 'snow.png'
        elif (WeatherData.isFreezingRain(list)):
            photoFileDay = 'rainPlusSnow.png'
        elif (WeatherData.isSleet(list)):
            photoFileDay = 'rainPlusSnow.png'
        else:
            photoFileDay = 'rainy.png'
    elif WeatherData.isCloudy(list):
        photoFileDay = 'cloudy.png'
    elif WeatherData.isPartlyCloudy(list):
        photoFileDay = 'partlySunny.png'
    elif WeatherData.isClear(list):
        photoFileDay = 'sunny.png'
    else:
        photoFileDay = 'sunny.png'

    return photoFileDay


def getNightImage(list):
    photoFileNight = ''


    if WeatherData.isStormy(list):
        photoFileNight = 'stormy.png'
    elif WeatherData.isRainy(list):
        if (WeatherData.isSnowy(list)):
            photoFileNight = 'snow.png'
        elif (WeatherData.isFreezingRain(list)):
            photoFileNight = 'rainPlusSnow.png'
        elif (WeatherData.isSleet(list)):
            photoFileNight = 'rainPlusSnow.png'
        else:
            photoFileNight = 'rainy.png'
    elif WeatherData.isCloudy(list):
        photoFileNight = 'cloudy.png'
    elif WeatherData.isPartlyCloudy(list):
        photoFileNight = 'partlyCloudyNight.png'
    elif WeatherData.isClear(list):
        photoFileNight = 'moon.png'
    else:
        photoFileNight = 'moon.png'

    return photoFileNight

def saveAndCreateImage():

    TwoInDisplay = LCD_2inch.LCD_2inch()
    WIDTH = TwoInDisplay.width
    HEIGHT = TwoInDisplay.height

    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT))
    img = ImageDraw.Draw(im)



    img.rectangle((5,5,WIDTH,HEIGHT), fill="white", outline="black", width=4)
#img.line((570,152,700,152), fill="gray", width= 2)
#img.line((570,240,700,240), fill="gray", width= 2)
#img.line((570,328,700,328), fill="gray", width= 2)
#img.line((287,65,287,415), fill="black", width= 4)
#img.line((570,65,570,415), fill="black", width= 4)
#img.line((352,15,352,65), fill="gray", width= 1)
#img.line((5,340,570,340), fill="black", width= 4)
#img.line((5,65,710,65), fill="black", width= 4)



# background_photo = PhotoImage(file='stormy.png')
# background = canvas.create_image(0,0,image=background_photo,anchor=NW)

    rainTotal = WeatherData.getRainTotal('https://www.wunderground.com/weather/us/in/west-lafayette')

#rainTotal = WeatherData.getRainTotal('https://www.wunderground.com/weather/us/wi/janesville')

    dayList = WeatherData.getDayList('https://www.timeanddate.com/sun/@4928096','https://forecast.weather.gov/MapClick.php?lat=40.4548&lon=-86.9157&lg=english&&FcstType=digital')

#dayList = WeatherData.getDayList('https://www.timeanddate.com/sun/usa/janesville','https://forecast.weather.gov/MapClick.php?lat=42.6879&lon=-89.0182&lg=english&&FcstType=digital')

#nightList = WeatherData.getNightList('https://www.timeanddate.com/sun/usa/janesville', 'https://forecast.weather.gov/MapClick.php?lat=42.6879&lon=-89.0182&lg=english&&FcstType=digital')

    nightList = WeatherData.getNightList('https://www.timeanddate.com/sun/@4928096', 'https://forecast.weather.gov/MapClick.php?lat=40.4548&lon=-86.9157&lg=english&&FcstType=digital')






# photo_image = PhotoImage(file='stormy.png').subsample(4,4)
# my_image = canvas.create_image(143,155,image=photo_image, anchor=CENTER)

# image_width = photo_image.width()
# image_height = photo_image.height()



    font = ImageFont.truetype('/home/huber93/SmallWaveshare/ShareTechMono-Regular.ttf',20)
#img.text((172, 40), text="Janesville, WI", fill="black", font=font, anchor="mm")
    img.text((WIDTH/2, 20), text="West Lafayette, IN", fill="black", font=font, anchor="mm")


    todaysDate = str(date.today())

    img.text((WIDTH/2, 50), text=todaysDate, fill="black", font=font, anchor="mm")

    if len(dayList) != 0:
        photoDay = getDayImage(dayList)
        dayWind = WeatherData.isWindy(dayList)
        highDay = WeatherData.getHigh(dayList)
        lowDay = WeatherData.getLow(dayList)



    photoNight = getNightImage(nightList)
    nightWind = WeatherData.isWindy(nightList)


    highNight = WeatherData.getHigh(nightList)
    lowNight = WeatherData.getLow(nightList)
    #sunrise = WeatherData.getSunsetRise('https://www.timeanddate.com/sun/usa/janesville')[0]
    #sunset = WeatherData.getSunsetRise('https://www.timeanddate.com/sun/usa/janesville')[1]
    sunrise = WeatherData.getSunsetRise('https://www.timeanddate.com/sun/@4928096')[0]
    sunrise = WeatherData.getSunsetRise('https://www.timeanddate.com/sun/@4928096')[1]
    #sunrise = 730
    #####sunset =800
    maxGust = WeatherData.maxGust(dayList + nightList)

    #realHigh = WeatherData.getRealHigh(dayList + nightList)
    #if realHigh is None:
        #realHigh = highDay


    #realLow = WeatherData.getRealLow(dayList + nightList)


    fontSmall = ImageFont.truetype('/home/huber93/SmallWaveshare/DejaVuSans.ttf',15)

#img.text((143, 80), text="Day", fill="black", font=fontSmall, anchor="mm")
#img.text((143, 83), text="____", fill="black", font=fontSmall, anchor="mm")
#img.text((425, 80), text="Night", fill="black", font=fontSmall, anchor="mm")
#img.text((425, 83), text="______", fill="black", font=fontSmall, anchor="mm")




    if (len(dayList) > 0):

        arialFontSlash = ImageFont.truetype('/home/huber93/SmallWaveshare/DejaVuSans.ttf',35)

        img.text((WIDTH*.25 + 3, HEIGHT/2 + 35), text="/", fill="gray", font=arialFontSlash, anchor="mm")
        img.text((WIDTH*.25 - 15, HEIGHT/2 + 35), text=str(highDay), fill="black", font=font, anchor="mm")
        img.text((WIDTH*.25 + 21, HEIGHT/2 + 35), text=str(lowDay), fill="black", font=font, anchor="mm")
    else:
        img.text((WIDTH*.25 + 7, HEIGHT/2), text="(It is Night)", fill="black", font=font, anchor="mm")

    arialFontSlash = ImageFont.truetype('/home/huber93/SmallWaveshare/DejaVuSans.ttf',35)
    img.text((WIDTH*.75 + 3, HEIGHT/2 + 35), text="/", fill="gray", font=arialFontSlash, anchor="mm")
    img.text((WIDTH*.75 - 5, HEIGHT/2 + 35), text=str(highNight), fill="black", font=font, anchor="rm")
    img.text((WIDTH*.75 + 11, HEIGHT/2 + 35), text=str(lowNight), fill="black", font=font, anchor="lm")


#img.text((637, 170), text="Sunrise", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 170), text="_______", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 205), text=str(sunrise) + 'a.m', fill="black", font=font, anchor="mm")

#img.text((637, 258), text="Sunset", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 258), text="_______", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 290), text=str(sunset) + 'p.m', fill="black", font=font, anchor="mm")

#img.text((637, 345), text="Max Gust", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 345), text="_________", fill="black", font=fontSmall, anchor="mm")
#img.text((638, 375), text=str(maxGust) + ' mph', fill="black", font=font, anchor="mm")



#img.text((637, 82), text="Td Rainfall", fill="black", font=fontSmall, anchor="mm")
#img.text((637, 82), text="___________", fill="black", font=fontSmall, anchor="mm")
#img.text((634, 120), text=str(rainTotal), fill="black", font=font, anchor="mm")


    arialFontSlashTwenty = ImageFont.truetype('/home/huber93/SmallWaveshare/DejaVuSans.ttf',20)


    arialFontSlashTwentyFive = ImageFont.truetype('/home/huber93/SmallWaveshare/DejaVuSans.ttf',25)

######img.text((427, 385), text="/", fill="gray", font=arialFontSlashTwentyFive, anchor="mm")
######img.text((418, 385), text=str(realHigh), fill="black", font=fontSmall, anchor="rm")
######img.text((434, 385), text=str(realLow), fill="black", font=fontSmall, anchor="lm")


#img.text((424, 355), text="Real-Feel", fill="black", font=fontSmall, anchor="mm")
#img.text((424, 358), text="__________", fill="black", font=fontSmall, anchor="mm")

#surfaceWind = WeatherData.getAverageWind(dayList + nightList)

#img.text((143, 355), text="Surface Wind", fill="black", font=fontSmall, anchor="mm")
#img.text((143, 358), text="____________", fill="black", font=fontSmall, anchor="mm")
#img.text((143, 385), text=str(surfaceWind) + " mph", fill="black", font=fontSmall, anchor="mm")


    im.save(r'/home/huber93/SmallWaveshare/finalDisplay.png', 'PNG')


    imageFinal = Image.open(r'/home/huber93/SmallWaveshare/finalDisplay.png')
#imageFinal = imageFinal.convert("RGBA")
    imageAddedNight = Image.open((r'/home/huber93/SmallWaveshare') + '/' + str(photoNight))
#imageAddedNight.convert("RGBA")
    imageAddedNight = imageAddedNight.resize((int(WIDTH/3),int(WIDTH/3)))
    imageFinal.paste(imageAddedNight, (int(WIDTH*.75) - 37, int(HEIGHT*.25)))

    if len(dayList) != 0:
        imageAddedDay = Image.open((r'/home/huber93/SmallWaveshare') + '/' + str(photoDay))
    #imageAddedDay.convert("RGBA")
        imageAddedDay = imageAddedDay.resize((int(WIDTH/3), int(WIDTH/3)))
        imageFinal.paste(imageAddedDay, (int(WIDTH*.25) - 37, int(HEIGHT*.25)))

# imageFinal.show()
    
    imageFinal = imageFinal.transpose(Image.FLIP_TOP_BOTTOM)
    imageFinal = imageFinal.transpose(Image.FLIP_LEFT_RIGHT)
    imageFinal.save(r'/home/huber93/SmallWaveshare/finalDisplay.png', 'PNG')

#imageFinal.show()



