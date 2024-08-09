from tkinter import *
from nfc_check import scanner
from db_connect import song_artist

root = Tk()

root.title("VinylInfoDisplay")
root.geometry('1920x1080')

def frame_gen(root):
    frame = Frame(root)
    frame.grid_rowconfigure(5, minsize=50)
    frame.grid_rowconfigure(9, minsize=50)
    frame.pack(side="top", expand=True, fill="both")
    return frame

def label_gen(frame):
    lbl = Label(frame, text = "Click to scan NFC")
    lbl.grid(column = 0, row = 0)

    #Album labels
    lbl2 = Label(frame, text = "")
    lbl2.grid(column = 0, row = 1)

    lblAlbumInfo = Label(frame, text = "")
    lblAlbumInfo.grid(column = 0, row = 2)

    lblTitleHeader = Label(frame, text = "")
    lblTitleHeader.grid(column = 0, row = 3)

    lblArtistHeader = Label(frame, text = "")
    lblArtistHeader.grid(column = 1, row = 3)

    lblRuntimeHeader = Label(frame, text = "")
    lblRuntimeHeader.grid(column = 2, row = 3)

    lblNoOfDiscsHeader = Label(frame, text = "")
    lblNoOfDiscsHeader.grid(column = 3, row = 3)

    lblDiscSizeHeader = Label(frame, text = "")
    lblDiscSizeHeader.grid(column = 4, row = 3)

    lblSpeedHeader = Label(frame, text = "")
    lblSpeedHeader.grid(column = 5, row = 3)

    lblNotesHeader = Label(frame, text = "")
    lblNotesHeader.grid(column = 6, row = 3)

    lblTitle = Label(frame, text = "")
    lblTitle.grid(column = 0, row = 4)

    lblArtist = Label(frame, text = "")
    lblArtist.grid(column = 1, row = 4)

    lblRuntime = Label(frame, text = "")
    lblRuntime.grid(column = 2, row = 4)

    lblNoOfDiscs = Label(frame, text = "")
    lblNoOfDiscs.grid(column = 3, row = 4)

    lblDiscSize = Label(frame, text = "")
    lblDiscSize.grid(column = 4, row = 4)

    lblSpeed = Label(frame, text = "")
    lblSpeed.grid(column = 5, row = 4)

    lblNotes = Label(frame, text = "")
    lblNotes.grid(column = 6, row = 4)

    lblGenreTitle = Label(frame, text = "")
    lblGenreTitle.grid(column = 0, row = 6)

    column = []
    
    lblTrackHeader = Label(frame, text = "")
    lblTrackHeader.grid(column = 0, row = 10)
    
    return lbl, lbl2, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblTitle, lblArtist, lblRuntime, lblNoOfDiscs, lblDiscSize, lblSpeed, lblNotes, lblGenreTitle, column, lblTrackHeader

def clicked(frame):
    lbl, lbl2, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblTitle, lblArtist, lblRuntime, lblNoOfDiscs, lblDiscSize, lblSpeed, lblNotes, lblGenreTitle, column, lblTrackHeader = label_gen(frame)
    frame.pack()
    
    uuid, record, genres, tracks = scanner()
    #lbl2.configure(text = "UUID: " + uuid)
    
    lblTitleHeader.configure(font = 'Calibri 14 bold', text = "Title")
    lblArtistHeader.configure(font = 'Calibri 14 bold', text = "Artist")
    lblRuntimeHeader.configure(font = 'Calibri 14 bold', text = "Runtime")
    lblNoOfDiscsHeader.configure(font = 'Calibri 14 bold', text = "Number of Discs")
    lblDiscSizeHeader.configure(font = 'Calibri 14 bold', text = "Disc Size")
    lblSpeedHeader.configure(font = 'Calibri 14 bold', text = "Speed")
    lblNotesHeader.configure(font = 'Calibri 14 bold', text = "Notes")
    
    for record_info in record:
            lblTitle.configure(text = record_info[0])
            lblArtist.configure(text = record_info[1])
            if record_info[2]:    
                m, s = divmod(record_info[2], 60)
                h, m = divmod(m, 60)
                lblRuntime.configure(text = f'{h:d}:{m:02d}:{s:02d}')
            lblNoOfDiscs.configure(text = str(record_info[3]))
            lblDiscSize.configure(text = str(record_info[4]) + '"')
            i, d = divmod(record_info[5], 1)
            if record_info[5] == 33.33:
                lblSpeed.configure(text = str(int(i)) + " 1/3 RPM")
            else:
                lblSpeed.configure(text = str(record_info[5]) + " RPM")
            lblNotes.configure(text = record_info[6])
            
    lblGenreTitle.configure(font = 'Calibri 14 bold', text = "Genres")
    
    for index, item in enumerate(genres):
        column = []
        for i, t in enumerate(genres[index]):
            column.append(Label(frame, text = t))
            if i == 1:
                if t != "Y":
                    column[0].configure(font = 'bold')
            else:
                column[i].grid(column = index, row = 7)
                
    lblTrackHeader.configure(font = 'Calibri 14 bold', text = "Tracks")
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
                        column[i].grid(column = it + i, row = index + 11)
            elif i == 2:
                if t:
                    m, s = divmod(int(t), 60)
                    column.append(Label(frame, text = f'{m:02d}:{s:02d}'))
                    column[i].grid(column = i, row = index + 11)
                else:
                    column.append(Label(frame, text = 'NULL'))
                    column[i].grid(column = i, row = index + 11)
            else:
                column.append(Label(frame, text = t))
                column[i].grid(column = i, row = index + 11)

def clear(frame):
    for widget in frame.winfo_children():
       widget.destroy()
    
    # button widget with red color text inside
    btn = Button(frame, text = "Scan" ,
             fg = "red", command=lambda:clicked(frame))
    # Set Button Grid
    btn.grid(column=3, row=0)
    
    # button widget with red color text inside
    btnClear = Button(frame, text = "Clear" ,
                 fg = "red", command=lambda:clear(frame))
    # Set Button Grid
    btnClear.grid(column=4, row=0)
    
    lbl, lbl2, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblTitle, lblArtist, lblRuntime, lblNoOfDiscs, lblDiscSize, lblSpeed, lblNotes, lblGenreTitle, column, lblTrackHeader = label_gen(frame)
    frame.pack()


frame = frame_gen(root)
lbl, lbl2, lblAlbumInfo, lblTitleHeader, lblArtistHeader, lblRuntimeHeader, lblNoOfDiscsHeader, lblDiscSizeHeader, lblSpeedHeader, lblNotesHeader, lblTitle, lblArtist, lblRuntime, lblNoOfDiscs, lblDiscSize, lblSpeed, lblNotes, lblGenreTitle, column, lblTrackHeader = label_gen(frame)

# button widget with red color text inside
btnClear = Button(frame, text = "Clear" ,
             fg = "red", command=lambda:clear(frame))
# Set Button Grid
btnClear.grid(column=4, row=0)
 
# button widget with red color text inside
btn = Button(frame, text = "Scan" ,
             fg = "red", command=lambda:clicked(frame))
# Set Button Grid
btn.grid(column=3, row=0)

frame.pack()
# Execute Tkinter
root.mainloop()