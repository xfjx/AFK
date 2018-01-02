#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import math
import sys

if len(sys.argv) != 2:
    print "Usage:", sys.argv[0],"STRING"
    exit()


# Welcome message
print "    _____"
print "   |     |"
print "   | | | |"
print "   |_____|"
print "   __|_|__ "
print "AFK - The automator for Kids!"
print
print "I can write a string to Mifare cards... beep beep beep..."
print 
print "WARNING!!! WRITING TO A CARD MAY BRICK IT! USE AT OWN RISK!!!"
print 
print "Press Ctrl-C to stop or place you card at the reader/writer to continue..."

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

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
        
        # Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()
    	
	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:

	    # Print UID
	    print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

    	    # This is the default key for authentication
    	    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
	    # Select the scanned tag
    	    size = MIFAREReader.MFRC522_SelectTag(uid)

    	    # Variable for the data to write
    	    string = sys.argv[1] 
	    blocksize = 16
	    block = 0

	    if (len(string) > (blocksize-1) * size):
		print "String is to long!"
		exit

	    for x in range(0, len(string)/blocksize+1):
		block += 1
		
		# Skip every last block of a sector or we will brick the card
		if (block+1) %4 == 0:
		    print "Skipping block", block
		    block += 1

	    	# Authenticate
		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)
    		print "\n"

		# Check if authenticated
    	    	if status == MIFAREReader.MI_OK:
    
    	    	    print "Block", block, " : ", string[x*blocksize:(x+1)*blocksize]
    
        	    data = map(ord,list(string[x*blocksize:(x+1)*blocksize]))
		    while (len(data) < blocksize):
			data.append(0x00)		

        	    print "Block",block,"will now be filled with the string:"

        	    # Write the data
	    	    MIFAREReader.MFRC522_Write(block, data)
    	    	    print "\n"
    
	    	    print "It now looks like this:"
    	    	    # Check to see if it was written
        	    MIFAREReader.MFRC522_Read(block)
        	    print "\n"

        	else:
	    	    print "Authentication error"

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
