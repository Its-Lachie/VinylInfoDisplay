from tkinter import *
from tkinter.scrolledtext import ScrolledText
from nfc_check import scanner
from db_connect import song_artist, collection_list

root = Tk()

root.title("VinylInfoDisplay")
root.geometry('1900x900')

text = ScrolledText(root, state='disable')
text.pack(side = "bottom", fill='both', expand=True)

def frame_gen(obj):
    frame = Frame(obj)
    return frame

def label_gen(frame):
    #Album labels
    lblUUIDHeader = Label(frame, font = 'Calibri 20 bold', text = "UUID: ")
    lblUUIDHeader.grid(column = 0, row = 1, pady = (5, 15))

    lblAlbumInfo = Label(frame, font = 'Calibri 20 bold', text = "Album Info")
    lblAlbumInfo.grid(column = 0, row = 2, pady = (5, 15))

    lblTitleHeader = Label(frame, font = 'Calibri 14 bold', text = "Title")
    lblTitleHeader.grid(column = 0, row = 3, padx = 15)

    lblArtistHeader = Label(frame, font = 'Calibri 14 bold', text = "Artist")
    lblArtistHeader.grid(column = 1, row = 3, padx = 15)

    lblRuntimeHeader = Label(frame, font = 'Calibri 14 bold', text = "Runtime")
    lblRuntimeHeader.grid(column = 2, row = 3, padx = 15)

    lblNoOfDiscsHeader = Label(frame, font = 'Calibri 14 bold', text = "Number of Discs")
    lblNoOfDiscsHeader.grid(column = 3, row = 3, padx = 15)

    lblDiscSizeHeader = Label(frame, font = 'Calibri 14 bold', text = "Disc Size")
    lblDiscSizeHeader.grid(column = 4, row = 3, padx = 15)

    lblSpeedHeader = Label(frame, font = 'Calibri 14 bold', text = "Speed")
    lblSpeedHeader.grid(column = 5, row = 3, padx = 15)

    lblNotesHeader = Label(frame, font = 'Calibri 14 bold', text = "Notes")
    lblNotesHeader.grid(column = 6, row = 3, padx = 15)

    lblGenreTitle = Label(frame, font = 'Calibri 14 bold', text = "Genres")
    lblGenreTitle.grid(column = 0, row = 6, padx = 15)
    
    lblTrackHeader = Label(frame, font = 'Calibri 14 bold', text = "Tracks")
    lblTrackHeader.grid(column = 0, row = 10, padx = 15)
    
    lblTrackNoHeader = Label(frame, font = 'Calibri 14 bold', text = "Track Number")
    lblTrackNoHeader.grid(column = 0, row = 11, padx = 15)
    
    lblTrackNameHeader = Label(frame, font = 'Calibri 14 bold', text = "Name")
    lblTrackNameHeader.grid(column = 1, row = 11, padx = 15)
    
    lblTrackLenHeader = Label(frame, font = 'Calibri 14 bold', text = "Length")
    lblTrackLenHeader.grid(column = 2, row = 11, padx = 15)
    
    lblTrackSideHeader = Label(frame, font = 'Calibri 14 bold', text = "Side of Record")
    lblTrackSideHeader.grid(column = 3, row = 11, padx = 15)
    
    lblTrackArtistHeader = Label(frame, font = 'Calibri 14 bold', text = "Artists")
    lblTrackArtistHeader.grid(column = 4, row = 11, padx = 15)
    
    return lblUUIDHeader, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblGenreTitle, lblTrackHeader, lblTrackNoHeader, lblTrackNameHeader, lblTrackLenHeader, lblTrackSideHeader, lblTrackArtistHeader 

def scan(root):
    global frame
    frame = frame_gen(text)
    text.window_create('1.0', window=frame)
    frame.grid_rowconfigure(5, minsize=50)
    frame.grid_rowconfigure(9, minsize=50)
    lblUUIDHeader, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblGenreTitle, lblTrackHeader, lblTrackNoHeader, lblTrackNameHeader, lblTrackLenHeader, lblTrackSideHeader, lblTrackArtistHeader = label_gen(frame)
    
    btnClear.config(command=lambda:clear(frame))
    btnAddToColl.config(command='')
    btnShowColl.config(command='')
    btnScan.config(command=lambda:rescan(frame, root))
    
    uuid, record, genres, tracks = scanner()
    
    lblUUIDHeader.configure(text = "UUID: ")
    data_string = StringVar()
    data_string.set(uuid)
    uuid_entry = Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len(uuid))
    uuid_entry.grid(column = 1, row = 1, pady = (5, 5))
    
    for index, record_info in enumerate(record):
        column = []
        for i, t in enumerate(record[index]):
            if i == 2:
                if t:
                    m, s = divmod(t, 60)
                    h, m = divmod(m, 60)
                    data_string = StringVar()
                    data_string.set(f'{h:d}:{m:02d}:{s:02d}')
                    column.append(Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len(f'{h:d}:{m:02d}:{s:02d}')))
                    column[i].grid(column = i, row = 4, padx = 5, sticky='ew')
                else:
                    data_string = StringVar()
                    data_string.set('------')
                    column.append(Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len('------')))
                    column[i].grid(column = i, row = 4, padx = 5, sticky='ew')
            elif i == 5:
                if t == 33.33:
                    data_string = StringVar()
                    data_string.set('33 1/3 RPM')
                    column.append(Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len(data_string.get())))
                    column[i].grid(column = i, row = 4, padx = 5, sticky='ew')
                else:
                    data_string = StringVar()
                    data_string.set(t+'RPM')
                    column.append(Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len(data_string.get())))
                    column[i].grid(column = i, row = 4, padx = 5, sticky='ew')
            else:
                data_string = StringVar()
                data_string.set(t)
                column.append(Entry(frame, textvariable=data_string, bd = 0, state="readonly", width = len(str(t))))
                column[i].grid(column = i, row = 4, padx = 5, sticky='ew')
    
    for index, item in enumerate(genres):
        column = []
        for i, t in enumerate(genres[index]):
            column.append(Label(frame, text = t))
            if i == 1:
                if t != "Y":
                    column[0].configure(font = 'bold')
            else:
                column[i].grid(column = index, row = 7)
                
    for index, item in enumerate(tracks):
        column = []
        for i, t in enumerate(tracks[index]):
            if i == 4:
                song_artists = song_artist(int(t))
                for it, artist in enumerate(song_artists):
                    if it > 0:
                        string = column[i].cget("text")
                        string = string + ", " + artist[0]
                        column[i].config(text = string)
                    else:
                        column.append(Label(frame, text = artist[0]))
                        column[i].grid(column = it + i, row = index + 12)
            elif i == 2:
                if t:
                    m, s = divmod(int(t), 60)
                    column.append(Label(frame, text = f'{m:02d}:{s:02d}'))
                    column[i].grid(column = i, row = index + 12)
                else:
                    column.append(Label(frame, text = '---'))
                    column[i].grid(column = i, row = index + 12)
            else:
                column.append(Label(frame, text = t))
                column[i].grid(column = i, row = index + 12)
                
def show_collection(root):
    global collection_frame
    collection_frame = frame_gen(text)
    text.window_create('1.0', window=collection_frame)
    
    btnClear.config(command=lambda:clear(collection_frame))
    btnScan.config(command='')
    btnAddToColl.config(command='')
    
    collection = collection_list()
    for index, item in enumerate(collection):
        column = []
        for i, t in enumerate(collection[index]):
            if i == 3:
                if t:    
                    m, s = divmod(t, 60)
                    h, m = divmod(m, 60)
                    data_string = StringVar()
                    data_string.set(f'{h:d}:{m:02d}:{s:02d}')
                    column.append(Entry(collection_frame, textvariable=data_string, bd = 0, state="readonly", width = len(f'{h:d}:{m:02d}:{s:02d}')))
                    column[i].grid(column = i, row = index, padx = 5, sticky='ew')
                else:
                    data_string = StringVar()
                    data_string.set('------')
                    column.append(Entry(collection_frame, textvariable=data_string, bd = 0, state="readonly", width = len('------')))
                    column[i].grid(column = i, row = index, padx = 5, sticky='ew')
            else:
                data_string = StringVar()
                data_string.set(t)
                column.append(Entry(collection_frame, textvariable=data_string, bd = 0, state="readonly", width = len(str(t))))
                column[i].grid(column = i, row = index, padx = 5, sticky='ew')
        
def add_to_collection():
    global add_collection_frame
    add_collection_frame = frame_gen(text)
    add_collection_frame.grid_rowconfigure(5, minsize=50)
    add_collection_frame.grid_rowconfigure(9, minsize=50)
    text.window_create('1.0', window=add_collection_frame)
    lblUUIDHeader, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblGenreTitle, lblTrackHeader, lblTrackNoHeader, lblTrackNameHeader, lblTrackLenHeader, lblTrackSideHeader, lblTrackArtistHeader = label_gen(add_collection_frame)
    
    btnClear.config(command=lambda:clear(add_collection_frame))
    btnScan.config(command='')
    btnShowColl.config(command='')
    
def rescan(frame_name, root):
    clear(frame_name)
    scan(root)

def clear(frame_name):
    for widget in frame_name.winfo_children():
       widget.destroy()
       
       frame_name.destroy()
       
    btnScan.configure(command=lambda:scan(root))
    btnShowColl.configure(command=lambda:show_collection(root))
    btnAddToColl.configure(command=add_to_collection)


root_frame = frame_gen(root)
root_frame.pack(side="top", fill="both")

# button widget with red color text inside
btnClear = Button(root_frame, text = "Clear" ,
             fg = "red")
# Set Button Grid
btnClear.grid(column=3, row=0, padx = 10)

# button widget with red color text inside
btnAddToColl = Button(root_frame, text = "Add to Collection" ,
             fg = "red", command=add_to_collection)
# Set Button Grid
btnAddToColl.grid(column=2, row=0, padx = 10)
 
# button widget with red color text inside
btnScan = Button(root_frame, text = "Scan NFC" ,
             fg = "red", command=lambda:scan(root))
# Set Button Grid
btnScan.grid(column=0, row=0, padx = (0,10))

# button widget with red color text inside
btnShowColl = Button(root_frame, text = "Show Collection" ,
             fg = "red", command=lambda:show_collection(root))
# Set Button Grid
btnShowColl.grid(column=1, row=0, padx = 10)


# Execute Tkinter
root.mainloop()