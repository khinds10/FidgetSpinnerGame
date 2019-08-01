#! /usr/bin/python
# player script to listen for select score board "type" button press
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import sys, time, json, string, cgi, subprocess, json, datetime, memcache
from gpiozero import Button
from Adafruit_LED_Backpack import AlphaNum4
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# setup the alphanumeric displays
displayOne = AlphaNum4.AlphaNum4(address=0x77)
displayOne.begin()
displayOne.set_brightness(8)
displayOne.clear()

displayTwo = AlphaNum4.AlphaNum4(address=0x76)
displayTwo.begin()
displayTwo.set_brightness(8)
displayTwo.clear()

def displayType(scoreBoardType):
    """set the ALPHNUM to scoreBoardType string value, with some padded spaces"""
    scoreBoardType = str(scoreBoardType)
    scoreBoardType = " " + scoreBoardType + "  "
    
    displayOne.clear()
    displayOne.print_str(scoreBoardType[0:4])
    displayOne.write_display()
    
    displayTwo.clear()
    displayTwo.print_str(scoreBoardType[4:8])
    displayTwo.write_display()

def select():
    """based on current game selected """
    scoreBoardType = mc.get("TYPE")

    if (scoreBoardType == "SCORE"):
        scoreBoardType = "TIMER"

    elif (scoreBoardType == "TIMER"):
        scoreBoardType = "CLEAR"

    elif (scoreBoardType == "CLEAR"):
        scoreBoardType = "SCORE"

    elif (scoreBoardType == "None"):
        scoreBoardType = "SCORE"

    mc.set("TYPE", scoreBoardType)
    displayType(scoreBoardType)
    

# set up defaults and show on alphanumeric display
mc.set("TYPE", "SCORE")
mc.set("PLAYER1", -1)
mc.set("PLAYER2", -1)

scoreBoardType = mc.get("TYPE")
displayType(scoreBoardType)

button = Button(17)
select()
while True:
    button.when_pressed = select
