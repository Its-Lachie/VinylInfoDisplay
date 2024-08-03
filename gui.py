from tkinter import *
from nfc_check import scanner

root = Tk()

root.title("VinylInfoDisplay")
root.geometry('1600x900')

lbl = Label(root, text = "Click to scan NFC")
lbl.grid(column = 0, row = 0)

#Album labels
lbl2 = Label(root, text = "")
lbl2.grid(column = 0, row = 1)

lblAlbumInfo = Label(root, text = "")
lbl2.grid(column = 0, row = 2)

lblTitleHeader = Label(root, text = "")
lblTitleHeader.grid(column = 0, row = 3)

lblArtistHeader = Label(root, text = "")
lblArtistHeader.grid(column = 1, row = 3)

lblRuntimeHeader = Label(root, text = "")
lblRuntimeHeader.grid(column = 2, row = 3)

lblNoOfDiscsHeader = Label(root, text = "")
lblNoOfDiscsHeader.grid(column = 3, row = 3)

lblDiscSizeHeader = Label(root, text = "")
lblDiscSizeHeader.grid(column = 4, row = 3)

lblSpeedHeader = Label(root, text = "")
lblSpeedHeader.grid(column = 5, row = 3)

lblNotesHeader = Label(root, text = "")
lblNotesHeader.grid(column = 6, row = 3)

lblTitle = Label(root, text = "")
lblTitle.grid(column = 0, row = 4)

lblArtist = Label(root, text = "")
lblArtist.grid(column = 1, row = 4)

lblRuntime = Label(root, text = "")
lblRuntime.grid(column = 2, row = 4)

lblNoOfDiscs = Label(root, text = "")
lblNoOfDiscs.grid(column = 3, row = 4)

lblDiscSize = Label(root, text = "")
lblDiscSize.grid(column = 4, row = 4)

lblSpeed = Label(root, text = "")
lblSpeed.grid(column = 5, row = 4)

lblNotes = Label(root, text = "")
lblNotes.grid(column = 6, row = 4)

lblGenreTitle = Label(root, text = "")
lblGenreTitle.grid(column = 0, row = 5)

lblGenreHeader = Label(root, text = "")
lblGenreHeader.grid(column = 0, row = 6)

lblSubgenreHeader = Label(root, text = "")
lblSubgenreHeader.grid(column = 1, row = 6)

column = []

def clicked():
    uuid, record, genres = scanner()
    lbl2.configure(text = "UUID: " + uuid)
    
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
    lblGenreHeader.configure(font = 'Calibri 14 bold', text = "Genre Name")
    lblSubgenreHeader.configure(font = 'Calibri 14 bold', text = "Subgenre?")
    
    for index, item in enumerate(genres):
        column = []
        for i, t in enumerate(genres[index]):
            column.append(Label(root, text = t))
            if t == "Y":
                column[i].grid(column = 1, row = index + 7)
            else:
                column[i].grid(row = index + 7)

def clear():
    lbl2.configure(text = "")
    lblTitle.configure(text = "")
    lblArtist.configure(text = "")
    lblRuntime.configure(text = "")
    lblNoOfDiscs.configure(text = "")
    lblDiscSize.configure(text = "")
    lblSpeed.configure(text = "")
    lblNotes.configure(text = "")
    lblTitleHeader.configure(text = "")
    lblArtistHeader.configure(text = "")
    lblRuntimeHeader.configure(text = "")
    lblNoOfDiscsHeader.configure(text = "")
    lblDiscSizeHeader.configure(text = "")
    lblSpeedHeader.configure(text = "")
    lblNotesHeader.configure(text = "")
    lblGenreTitle.configure(text = "")
    lblGenreHeader.configure(text = "")
    lblSubgenreHeader.configure(text = "")
    #Clear genre columns not working
    for label in column:
        label.configure(text = "")

# button widget with red color text inside
btnClear = Button(root, text = "Clear" ,
             fg = "red", command=clear)
# Set Button Grid
btnClear.grid(column=4, row=0)
 
# button widget with red color text inside
btn = Button(root, text = "Scan" ,
             fg = "red", command=clicked)
# Set Button Grid
btn.grid(column=3, row=0)

# Execute Tkinter
root.mainloop()