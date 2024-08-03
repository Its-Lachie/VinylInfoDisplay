from fractions import Fraction
import sqlite3

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
        record_list = list(record)
        
        # Genres
        genres = conn.execute("SELECT genre_name, subgenre FROM genres WHERE uuid = ?", (uuid,))
        record_genres = list(genres)
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
    return uuid, record_list, record_genres