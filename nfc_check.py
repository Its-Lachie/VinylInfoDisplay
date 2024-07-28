# This is where the NFC reader code will run
import RPi.GPIO as GPIO
from pn532 import *
import sqlite3

debug = True

def database_check(hexVal):
    conn = sqlite3.connect('database/collection.db')
    
    idCheck = conn.execute("SELECT uuid FROM idCheck WHERE nfcID = ?", (hexVal,)) 
    for idChecked in idCheck:
        uuid = idChecked[0]
        print("UUID: ", uuid)
        print("----------------")
        
        record = conn.execute("SELECT title, artist, runtime, number_of_discs, disc_size FROM collection WHERE uuid = ?", (uuid,))
        for record_info in record:
            print("Title: ", record_info[0])
            print("Artist: ", record_info[1])
            m, s = divmod(record_info[2], 60)
            h, m = divmod(m, 60)
            print("Runtime: ", f'{h:d}:{m:02d}:{s:02d}')
            print("Number of Discs: ", record_info[3])
            print("Disc Size: ", str(record_info[4])+'"')
            print(" ")
            print("Tracks:")

        # TO DO: ADD TRACK NUMBER COLUMN
        tracklist = conn.execute("SELECT trackid, title, track_length, side_of_record FROM tracks WHERE uuid = ?", (uuid,))
        for track in tracklist:
            trackid = track[0]
            print("Track ID: ", trackid)
            print("Song Name: ", track[1])
            print("Song Artists: ")
            song_artists = conn.execute("SELECT artist from track_artist WHERE trackID = ?", (trackid,))
            for artist in song_artists:
                print("   ", artist[0])
            m, s = divmod(track[2], 60)
            print("Track Length: ",f'{m:02d}:{s:02d}')
            print("Side of Record: ", track[3])
            print("~~~~~~~~~~~~~~~~~~~")
        
    conn.close()

if __name__ == '__main__':
    try:        
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC tag...')
        tagChecking = True
        while tagChecking:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print(' ')
            # Try again if no card is available.
            if uid is None:
                continue
            else:
                hexValList = [hex(i) for i in uid]
                hexVal = "-".join(hexValList)
                
                if debug:
                    print('Base UID: ', uid)
                    print('Found card with UID:', [hex(i) for i in uid])
                    print('hexValList: ', hexValList)
                    print('hexVal: ', hexVal)
                
                database_check(hexVal)
                tagChecking = False
           
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
