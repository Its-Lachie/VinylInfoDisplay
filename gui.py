from tkinter import *
from nfc_check import scanner

root = Tk()

root.title("VinylInfoDisplay")
root.geometry('1600x900')

lbl = Label(root, text = "Click to scan NFC")
lbl.grid(column = 0, row = 0)

lbl2 = Label(root, text = "")
lbl2.grid(column = 0, row = 1)

lblTitle = Label(root, text = "")
lblTitle.grid(column = 0, row = 2)

lblArtist = Label(root, text = "")
lblArtist.grid(column = 1, row = 2)

lblRuntime = Label(root, text = "")
lblRuntime.grid(column = 2, row = 2)

lblNoOfDiscs = Label(root, text = "")
lblNoOfDiscs.grid(column = 3, row = 2)

lblDiscSize = Label(root, text = "")
lblDiscSize.grid(column = 4, row = 2)

lblSpeed = Label(root, text = "")
lblSpeed.grid(column = 5, row = 2)

lblNotes = Label(root, text = "")
lblNotes.grid(column = 6, row = 2)

def clicked():
    uuid, record = scanner()
    lbl2.configure(text = "UUID: " + uuid)
    
    for record_info in record:
            lblTitle.configure(text = "Title: " + record_info[0])
            lblArtist.configure(text = "Artist: " + record_info[1])
            m, s = divmod(record_info[2], 60)
            h, m = divmod(m, 60)
            lblRuntime.configure(text = "Runtime: " + f'{h:d}:{m:02d}:{s:02d}')
            lblNoOfDiscs.configure(text = "Number of Discs: " + str(record_info[3]))
            lblDiscSize.configure(text = "Disc Size: " + str(record_info[4]) + '"')
            i, d = divmod(record_info[5], 1)
            if record_info[5] == 33.33:
                lblSpeed.configure(text = "Speed: " + str(int(i)) + " 1/3 RPM")
            else:
                lblSpeed.configure(text = "Speed: " + str(record_info[5]) + " RPM")
            lblNotes.configure(text = "Notes: " + record_info[6])

def clear():
    lbl2.configure(text = "")
    lblTitle.configure(text = "")
    lblArtist.configure(text = "")
    lblRuntime.configure(text = "")
    lblNoOfDiscs.configure(text = "")
    lblDiscSize.configure(text = "")
    lblSpeed.configure(text = "")
    lblNotes.configure(text = "")

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