# AFK
AFK - The Automator For Kids using NFC tags 

This repository holds everything I needed to create a NFC powered automator for kids.

You can create a music box, a simple remote for your Sonos speakers and home automation system or what ever cool idea you up with! I will put a link to some youtube videos of my projects.

Disclaimer: I am not the best at python programming so my code might be terrible! See this whole projekt as a starting point for your own ideas and let me know if you used it.

The MFRC522.py is taken from [MFRC522-python](https://github.com/mxgxw/MFRC522-python).

## How this works
All you need is a Raspberry PI (I tried PI 2,PI 3 and PI Zero W) with a MFRC522 reader. When you hold the card near your reader it will get recognized and some action should be triggered.

There are two ways to define the action you want to execute:

1. Just place a script with the UID of the card in the actions/uid/ folder (e.g. ./actions/uid/AA_BB_CC_DD) and make it run able (chmod 755).
2. Write an URL or AFK-action to the card
3. Use a sqlite db to map card UIDs to actions

All actions are placed with the ./actions folder. You can create sub folders to group actions of a certain kind. If you use sub folders just put the whole name of the action on your card or the mapping db (e.g. mpd/album).

Every action takes an argument. The syntax for that is action:argument (e.g. mpd/album:Giraffenaffen). 

I included some actions I created for my own use - as these actions are simple scripts (bash, python, perl, ...) you can easily expand the system to your own needs.

If no script for the UID is found and there is nothing on the NFC card I will call the default action. I included a sample that uses sqlite3 to search in a mapping db for an action for that uid. If you place a new card in front of the reader for the first time it will create an empty record in the db for that UID.

I KNOW THAT IT MIGHT BE A SECURITY ISSUE TO EXECUTE A SCRIPT BASED ON THE INFORMATION ON A NFC CARD. IT MIGHT BE POSSIBLE TO INJECT CODE OR CALL PROGRAMS THAT YOU DID NOT WANT TO BE CALLED. PLEASE ADD YOUR OWN SECURITY LAYER IF YOU THINK THAT IS NECESSARY.

## About Mifare Cards
OK, Mifare Classic 1K cards are really cheap so they are just perfekt for this project. But: I didn't find an implementation of how to write large strings to them. The trick is to skip every last block of a sector (the sector trailer) because he holds the keys and permissions for that sector.
After bricking about 5 NFC tags I was able to write about 700 bytes to a card.

I created the little script WriteStringToMifare.py for that task. The cool thing about using a NFC card which hold an URL or AFK action is that you do not need to access the AFK system if you want to add a new card. Of cause it is possible to use Wifi with your Pi or even write your own management web interface for that task. I created a little default action which uses a sqlite database to search for a mapping of the UID to an action.
