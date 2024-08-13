# This is where the NFC reader code will run
import RPi.GPIO as GPIO
from pn532 import *
import pn532.pn532 as nfc
from db_connect import database_check

debug = True

def scan():
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

                    tagChecking = False
               
        except Exception as e:
            print(e)
            continue
        finally:
            GPIO.cleanup()
        break
    return hexVal
    
def write(hexList):
    scanning = True
    while scanning:
        try:
            pn532 = PN532_SPI(debug=False, reset=20, cs=4)

            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with NTAG215 cards
            pn532.SAM_configuration()

            print('Waiting for RFID/NFC card to write to!')
            tagChecking = True
            while tagChecking:
                # Check if a card is available to read
                uid = pn532.read_passive_target(timeout=0.5)
                print('.', end="")
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
                    
                    tagChecking = False
                    
        except Exception as e:
            print(e)
            continue
        finally:
            scanning = False
            writing = True
    
    # Write block #6
    block_number = 6
    data = bytes(hexList)
    print("Data:", data)

    while writing:
        try:
            print("Trying to write")
            pn532.ntag2xx_write_block(block_number, data)
            if pn532.ntag2xx_read_block(block_number) == data:
                print('write block %d successfully' % block_number)
        except nfc.PN532Error as e:
            print(e.errmsg)
            continue
        finally:
            GPIO.cleanup()
            writing = False
            break

def scan_record():
    hexVal = scan()
    uuid, record, genres, tracks = database_check(hexVal)
    return uuid, record, genres, tracks, hexVal

def get_hexVal():
    hexVal = scan()
    return hexVal

def change_hexVal(newHexVal):
    print("New hexVal:", newHexVal)
    newHexValList = newHexVal.split("-")
    hexList = [int(x, 16) for x in newHexValList]
    print("New hexVal as list:", hexList)
    write(hexList)
