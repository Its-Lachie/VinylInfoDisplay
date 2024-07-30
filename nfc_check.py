# This is where the NFC reader code will run
import RPi.GPIO as GPIO
from pn532 import *
from fractions import Fraction
import sqlite3
#import tkinter as tk

debug = True

def database_check(hexVal):
    # To implement: GUI interface
    #window = tk.Tk()
    #text_box = tk.Text()
    #text_box.pack()
    
    conn = sqlite3.connect('database/collection.db')
    
    idCheck = conn.execute("SELECT uuid FROM idCheck WHERE nfcID = ?", (hexVal,)) 
    for idChecked in idCheck:
        uuid = idChecked[0]
        #text_box.insert("1.0", "UUID: "+uuid)
        print("UUID: ", uuid)
        print("----------------")
        print(" ")
        
        # Record Info
        record = conn.execute("SELECT title, artist, runtime, number_of_discs, disc_size, speed, notes FROM collection WHERE uuid = ?", (uuid,))
        for record_info in record:
            print("Title: ", record_info[0])
            print("Artist: ", record_info[1])
            m, s = divmod(record_info[2], 60)
            h, m = divmod(m, 60)
            print("Runtime: ", f'{h:d}:{m:02d}:{s:02d}')
            print("Number of Discs: ", record_info[3])
            print("Disc Size: ", str(record_info[4])+'"')
            i, d = divmod(record_info[5], 1)
            if record_info[5] == 33.33:
                print("Speed: ", str(int(i))+" 1/3 RPM")
            else:
                print("Speed: ", record_info[5], "RPM", d)
            print("Notes: ", record_info[6])
        
        # Genres
        genres = conn.execute("SELECT genre_name, subgenre FROM genres WHERE uuid = ?", (uuid,))
        for genre_info in genres:
            if genre_info[1] == "Y":
                print("   Subgenre: ", genre_info[0])
            else:
                print("Genre: ", genre_info[0])
            
        print("-------------------------------")
        print("Tracks:")
        print("")

        # Tracklist
        side = ""
        tracklist = conn.execute("SELECT trackid, track_number, title, track_length, side_of_record FROM tracks WHERE uuid = ?", (uuid,))
        for track in tracklist:
            if track[4] != side and side != "":
                print("")
                print("")
                side = track[4]
            else:
                print("~~~~~~~~~~~~~~~~~~~")
                side = track[4]
                
            trackid = track[0]
            print("Track ID: ", trackid)
            print("Track Number: ", track[1])
            print("Song Name: ", track[2])
            print("Song Artists: ")
            song_artists = conn.execute("SELECT artist, main, featured, remixer from track_artist WHERE trackID = ?", (trackid,))
            for artist in song_artists:
                if artist[2] == "Y":
                    print("    ft.", artist[0])
                elif artist[3] == "Y":
                    if artist[1] == "Y":
                        print("   ", artist[0])
                    print("Remixed by:", artist[0])
                else:
                    print("   ", artist[0])
            m, s = divmod(track[3], 60)
            print("Track Length: ",f'{m:02d}:{s:02d}')
            print("Side of Record: ", track[4])
            
            
                
        
    conn.close()

def scanner():
    while True:
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
            continue
        finally:
            GPIO.cleanup()
        break

if __name__ == '__main__':    
    scanner()