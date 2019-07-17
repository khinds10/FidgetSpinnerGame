#! /usr/bin/python
# Player script to listen for button press, then start the timers
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0

import time, datetime
import os, signal, atexit, psutil
import subprocess
from gpiozero import Button
from Adafruit_LED_Backpack import SevenSegment

playerOneMinutes = SevenSegment.SevenSegment(address=0x74)
playerOneMinutes.begin()
playerOneMinutes.clear()
playerOneMinutes.write_display()

playerOneSeconds = SevenSegment.SevenSegment(address=0x70)
playerOneSeconds.begin()
playerOneSeconds.clear()
playerOneSeconds.write_display()

def resetTimer():
    """setup the display and begin the timer starting from zero """
    global minutesOutputPrevious
    global startTime
    global milleseconds
    
    minutesOutputPrevious = ''
    startTime = 0
    milleseconds = 0
    
    playerOneMinutes.set_colon(True)
    playerOneMinutes.write_display()
    playerOneSeconds.set_colon(True)
    playerOneSeconds.write_display()

    zeroChars = [0,0,0,0]
    count = 0
    while (count < 4):
        playerOneMinutes.set_digit(count, zeroChars[count])
        playerOneSeconds.set_digit(count, zeroChars[count])
        count = count + 1
    playerOneMinutes.write_display()
    playerOneSeconds.write_display()
    
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
                playerOneMinutes.set_digit(count, minutesOutput[count])
                count = count + 1
            playerOneMinutes.write_display()
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
            playerOneSeconds.set_digit(count, secondsOutputChars[count])
            count = count + 1
        playerOneSeconds.write_display()

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
        resetTimer()        
    timerState = timerState + 1
    if timerState > 2:
        timerState = 0

button = Button(24)
resetTimer()
while True:
    button.when_pressed = timer

