# Vinyl Info Display
Vinyl Info Display - NFC Reader to show info about your vinyl records as they are played

## What is VinylInfoDisplay?
VinylInfoDisplay is a home project I am working on to showcase my record collection in a new way. The end goal here is to create a display stand for a specified record's "album art" as it is being played, that has a screen to display information about the album (track list, track lengths, artists, genres). With this application, the possibilities of what information that can be displayed are endless.

## What technology is being used here?
This specific application is using a Raspberry Pi 4 and Waveshare PN542 NFC Hat. The application is run in Python, and the idea is to scan the vicinity of the reader for an NFC tag/sticker located on a record's outer protective sleeve. Once the tag has been picked up, the application will access the SQLite database to grab information, which will then be displayed in a front-end GUI. This is currently being run with TKinter.

I am still working out the best way to display the information in the end, whether I use a built in GUI or a localhost website that any device can load up. Along with this, still havent decided on a screen size for this, whether it links to a small screen or monitor next to the RPi device or to run it in full 16:9 on a nearby TV.

## What should the database look like?
Mine is a SQLite 3 database, which has been added here as "sample_collection.db". You can build on your own collection with this template, or customise to your hearts content.