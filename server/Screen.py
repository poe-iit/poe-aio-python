import tkinter as tk
from tkinter import *
import tkinter.font as font
import threading

from server import Server


# Important that all list indexes line up with each other (buttonList[i] -> labelList[i])
colours = ['red', 'green', 'orange', 'white'] # List of the button colours
labelList = ['Fire', 'Extreme Weather', 'Active shooter', 'Public Safety'] # List of the button labels
buttonList = [] # List of the buttons
frameList = [] # List of the frames
activeList = [False, False, False, False] # List to check status of buttons

root = tk.Tk()
root.attributes('-fullscreen', True) # auto-set to fullscreen

h = root.winfo_screenheight()
w = root.winfo_screenwidth()
root.geometry(str(w) + 'x' + str(h)) # Setting the window size

root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False)) # Pressing Escape turns off fullscreen
root.bind("<Enter>", lambda event: root.attributes('-fullscreen', True)) # Pressing Enter turns on fullscreen
root.bind("<Delete>", lambda event: root.destroy()) # Pressing Delete closes the window

helv = font.Font(family = 'Helvetica', size = 24, weight = "bold") # Font settings


def statusCheck(check, bIndex, msg): #Checks whether to flip the status, and flips it
    global buttonList, activeList, labelList, colours
    if check:
        cButton = buttonList[bIndex]
        cButton.config(bg = colours[bIndex])
        activeList[bIndex] = True
        Server.alert_client_2() #send emergency type to client 2


    msg.destroy()

def status(l): #Creates button for statusCheck to flip status of button
    global buttonList, activeList, labelList, colours, w, h, helv
    bIndex = labelList.index(l) # Finds button
    # Flips the status of button
    if not activeList[bIndex]: #Creates the pop-up for statusCheck
        msg = tk.Tk()
        msg.geometry(str(w // 4) + 'x' + str(h // 4))
        label = tk.Label(msg, text = l, font = helv)
        label.pack(fill = "x", pady = h // 16)
        B1 = tk.Button(msg, text = "Okay", command = lambda bIndex = bIndex: statusCheck(True, bIndex, msg))
        B2 = tk.Button(msg, text = "Cancel", command = lambda bIndex = bIndex: statusCheck(False, bIndex, msg))
        B1.pack(side = 'left', fill = 'both', expand = 1)
        B2.pack(side = 'right', fill = 'both', expand = 1)
        msg.mainloop()
    else: #If already active, it will change it to non-active
        cButton = buttonList[bIndex]
        cButton.config(bg = 'gray')
        activeList[bIndex] = False



def start_GUI():

    for i in range(4): # Makes all 4 buttons and frames
        c = colours[i]
        l = labelList[i]
        # Frame
        newFrame = Frame(root)
        newFrame.grid(row = i // 2, column = i % 2, sticky = "NSEW")
        frameList.append(newFrame)
        # Button
        newButton = tk.Button(frameList[i], text = l, font = helv, bg = 'gray', command = lambda l = l: status(l))
        newButton.pack(fill = BOTH, expand = 1)
        buttonList.append(newButton)

    for i in range(2): # Makes sure that frame and buttons fill their grid positions
        root.rowconfigure(i, weight = 1)
        root.columnconfigure(i, weight = 1)
    root.mainloop()


def main():
    process = threading.Thread(target=Server.main)
    process.start()
    start_GUI()


if __name__ == '__main__':
    main()
