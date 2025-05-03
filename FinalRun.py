import os
import sys 
import time
import logging
import spidev as SPI
import Display
from WaveshareModule import LCD_2inch
from PIL import Image

if __name__ == '__main__':
    
    RST = 27
    DC = 25
    BL = 18
    bus = 0 
    device = 0 

    Display.saveAndCreateImage()
    #image = Image.open(r'home/riley/Weather/finalDisplay.png')
    image = Image.open(r'/home/huber93/SmallWaveshare/finalDisplay.png')
    
    #disp = LCD_2inch4.LCD_2inch4()
    disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp.Init()
    disp.clear()
    disp.bl_DutyCycle(50)
    disp.ShowImage(image)
    time.sleep(1740)
    disp.module_exit()
    
    
