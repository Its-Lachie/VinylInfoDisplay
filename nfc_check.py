# This is where the NFC reader code will run
import RPi.GPIO as GPIO
from pn532 import *

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
                print('Base UID: ', uid)
                print('Found card with UID:', [hex(i) for i in uid])
                hexVal = [hex(i) for i in uid]
                print('hexVal: ', hexVal)
                print('hexVal as joined string: ', "-".join(hexVal))
                tagChecking = False
           
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
