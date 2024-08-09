from fractions import Fraction
import sqlite3

def connection_init():
    conn = sqlite3.connect('database/collection.db')
    return conn

def database_check(hexVal):
    # To implement: GUI interface
    #window = tk.Tk()
    #text_box = tk.Text()
    #text_box.pack()
    
    conn = connection_init()
    
    idCheck = conn.execute("SELECT uuid FROM idCheck WHERE nfcID = ?", (hexVal,)) 
    for idChecked in idCheck:
        uuid = idChecked[0]
        #text_box.insert("1.0", "UUID: "+uuid)
        print("UUID: ", uuid)
        
        # Record Info
        record = conn.execute("SELECT title, artist, runtime, number_of_discs, disc_size, speed, notes FROM collection WHERE uuid = ?", (uuid,))
        record_list = list(record)
        
        # Genres
        genres = conn.execute("SELECT genre_name, subgenre FROM genres WHERE uuid = ?", (uuid,))
        record_genres = list(genres)

        # Tracklist
        side = ""
        tracklist = conn.execute("SELECT track_number, title, track_length, side_of_record, trackid FROM tracks WHERE uuid = ?", (uuid,))
        tracks = list(tracklist)
            
    conn.close()
    return uuid, record_list, record_genres, tracks

def song_artist(trackID):
    conn = connection_init()
    song_artists = conn.execute("SELECT artist, main, featured, remixer from track_artist WHERE trackID = ?", (trackID,))
    artists = list(song_artists)
    return artists

def collection_list():
    conn = connection_init()
    collection = conn.execute("SELECT * from collection")
    collectionList = list(collection)
    return collectionList