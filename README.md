# AFK
AFK - The Automator For Kids using NFC tags 

This repository holds everything I needed to create a NFC powered automator for kids. You can create a musicbox, a simple remote for your sonos spearkers and home automation system or what ever cool idea you up with! I will put a link to some youtube videos of my projects.

## How this works
All you need is a Raspberry PI (I tried PI 2,PI 3 and PI Zero W) with a MFRC522 reader. When you hold the card near your reader it will get recognized and some action should be triggered.

There are two ways to define the action you want to excecute:

1) Just place a script with the UID of the card in the actions/uid/ folder (e.g. ./actions/uid/AA_BB_CC_DD) and make it runable (chmod 755).
2) Write an URL or AFK-action to the card   

## About Mifare Cards
OK, Mifare Classic 1K cards are really cheap so they are just perfekt for this projekt. But: I didn't find a implemantion of how to write large strings to them. The trick is to skip every last block of a sector (the sector trailer) because the hold the keys and permissions for that sector.
After bricking about 5 NFC tags I was able to write about 700 bytes to a card.

I created the little script WriteStringToMifare.py for that task. The cool thing about using a NFC card which hold an URL or AFK action is that you do not need to access the AFK system if you want to add a new card. Of couse it is possible to use Wifi with your Pi or even write your own managemnt web interface for that task. I created a little default action which uses a sqlite database to search for a mapping of the UID to an action.
