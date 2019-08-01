#! /usr/bin/python
# player script to listen for button press, then start the timer or scoreboard
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0

import time, datetime, sys, json, string, cgi, subprocess, json, datetime, memcache
import os, signal, atexit, psutil
import subprocess
from gpiozero import Button
from Adafruit_LED_Backpack import SevenSegment
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

playerMinutes = SevenSegment.SevenSegment(address=0x74)
playerMinutes.begin()
playerMinutes.clear()
playerMinutes.write_display()

playerSeconds = SevenSegment.SevenSegment(address=0x70)
playerSeconds.begin()
playerSeconds.clear()
playerSeconds.write_display()

def clearDisplay():
    """setup the display and begin the display starting from zero"""
    global minutesOutputPrevious
    global startTime
    global milleseconds
    
    minutesOutputPrevious = ''
    startTime = 0
    milleseconds = 0
    
    playerMinutes.set_colon(True)
    playerMinutes.write_display()
    playerSeconds.set_colon(True)
    playerSeconds.write_display()

    zeroChars = [0,0,0,0]
    count = 0
    while (count < 4):
        playerMinutes.set_digit(count, zeroChars[count])
        playerSeconds.set_digit(count, zeroChars[count])
        count = count + 1
    playerMinutes.write_display()
    playerSeconds.write_display()
    
def runTimer():
    """run the timer showing number of seconds on the 7 segment display"""
    global minutesOutputPrevious
    global startTime
    global milleseconds
    while True:

        # from the start of the script, get the time in seconds, milleseconds to display
        if (startTime == 0):
            startTime = time.time()
        elapsedTime = time.time() - startTime
            
        # write the 4 digits individually to the display, but only if they've changed
        minutesOutput = str(time.strftime("%H%M", time.gmtime(elapsedTime)))
        if minutesOutputPrevious != minutesOutput:
            count = 0
            minutesOutputChars = list(minutesOutput)
            while (count < 4):
                playerMinutes.set_digit(count, minutesOutput[count])
                count = count + 1
            playerMinutes.write_display()
            minutesOutputPrevious = minutesOutput
        
        # keep track of hypothetical milleseconds (they won't be 100% accurate based on script speed)
        milleseconds = milleseconds + 1
        if milleseconds > 99: 
            milleseconds = 1 
        secondsOutput = str(time.strftime("%S", time.gmtime(elapsedTime))) + str('%02d' % milleseconds)
        
        # write the 4 digits individually to the display
        count = 0
        secondsOutputChars = list(secondsOutput)
        while (count < 4):
            playerSeconds.set_digit(count, secondsOutputChars[count])
            count = count + 1
        playerSeconds.write_display()

timerState = 0
processId = False
def timer():
    global timerState
    global processId
    
    if timerState == 0:
        processId = os.fork()
        if processId == 0:
            runTimer()
            
    if timerState == 1:
        if processId > 0:
            os.kill(processId, signal.SIGKILL)
    
    if timerState == 2:
        clearDisplay()        
    timerState = timerState + 1
    if timerState > 2:
        timerState = 0

def setScore(score):
    """set the score int to the display"""
    playerSeconds.clear()
    count = 0
    while (count < 4):
        playerMinutes.set_digit(count, " ")
        count = count + 1
    playerMinutes.set_colon(False)
    playerMinutes.write_display()    
    playerSeconds.print_float(int(score), decimal_digits=0)
    playerSeconds.write_display()

def score():
    playerScore = mc.get("PLAYER1")
    playerScore = playerScore + 1
    mc.set("PLAYER1", playerScore)
    setScore(playerScore)

def clear():
    mc.set("PLAYER1", -1)
    clearDisplay()
    
button = Button(24)
clearDisplay()
while True:
    scoreBoardType = mc.get("TYPE")
    if (scoreBoardType == "SCORE"):
        button.when_pressed = score
        
    elif (scoreBoardType == "TIMER"):
        button.when_pressed = timer
        
    elif (scoreBoardType == "CLEAR"):
        button.when_pressed = clear
