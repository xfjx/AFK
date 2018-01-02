#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import os.path
import subprocess
from urlparse import urlparse
import urllib2

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "    _____"
print "   |     |"
print "   | | | |"
print "   |_____|"
print "   __|_|__ "
print "Welcome to AFK, the Automator For Kids!"
print
print "MFRC522 reader started... beep beep beep..."
print ""
print "Press Ctrl-C to stop."
print
print "Waiting for a card..."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:


    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    time.sleep(1)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:

    	    # Print UID
    	    print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    
	    # Check we have an action defined for that card
	    action = "./actions/uid/"+str(uid[0])+"_"+str(uid[1])+"_"+str(uid[2])+"_"+str(uid[3])
    	    if os.path.isfile(action):
		print "Found predefined action for UID!"
		print "Launching",action,"..."
		subprocess.Popen(action)

	    # We do not have an action defined for the card, lets check the content of the card...
	    else:
        	# This is the default key for authentication
		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
    	        # Select the scanned tag
    		MIFAREReader.MFRC522_SelectTag(uid)

		size = 63
    		block = 1
    		done = False
    		string = ""
    
    		while (not done and block <= size):
	    
		    # Skip every last block of a sector, there is no data for us
		    if (block+1) % 4 == 0:
			print "Skipping block", block
			block += 1

		    # Authenticate
    		    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)
	
        	    # Check if authenticated
	    	    if status == MIFAREReader.MI_OK:
			data = MIFAREReader.MFRC522_Read(block)
			block = block+1
			done = (0x00 in data)
			for char in data:
			    if char != 0x00:
				string+=chr(char)

    		    else:
        		print "Authentication error"


		if string:
		    # Valid commands are URLs or "directory/action:parameter" e.g. "mpd/album:Wo ist Kartoffelbrei" or "sonos/applemusic:1143577200"
		    print "Found string",string,"on card!"
		
		    # URL
		    if string[:4] == "http":
			urllib2.urlopen(string)
		    else:
			action = string.split(':')
			action[0] = "./actions/"+action[0]
			if os.path.isfile(action[0]):
			    print "Launching",action,"..."
		    	    subprocess.Popen(action)
		else:
		    action = ["./actions/default",str(uid[0])+"_"+str(uid[1])+"_"+str(uid[2])+"_"+str(uid[3])]
		    if os.path.isfile(action[0]):
			print "Launching",action,"..."
		    	subprocess.Popen(action)

    	    MIFAREReader.MFRC522_StopCrypto1()

	time.sleep(5)
	print "Waiting for a card..."


