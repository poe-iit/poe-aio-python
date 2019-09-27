import tkinter as tk
from tkinter import *
import tkinter.font as font

def status(l): #Flips the status of a button between active or idle and creates a pop up
    global buttonList, activeList, labelList, colours
    bIndex = labelList.index(l) # Finds button
    # Flips the status of button
    if not activeList[bIndex]:
        cButton = buttonList[bIndex]
        cButton.config(bg = colours[bIndex])
        activeList[bIndex] = True
        # Makes pop-up if status flipped to true
        msg = tk.Tk()
        label = tk.Label(msg, text = l)
        label.pack(side = "top", fill = "x", pady = 10)
        B1 = tk.Button(msg, text = "Okay", command = msg.destroy)
        B1.pack()
        msg.mainloop()
    else:
        cButton = buttonList[bIndex]
        cButton.config(bg = 'gray')
        activeList[bIndex] = False
    
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
root.geometry(str(root.winfo_screenwidth()) + 'x' + str(root.winfo_screenheight())) # Setting the window size

root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False)) # Pressing Escape turns off fullscreen
root.bind("<Enter>", lambda event: root.attributes('-fullscreen', True)) # Pressing Enter turns on fullscreen
root.bind("<Delete>", lambda event: root.destroy()) # Pressing Delete closes the window

helv = font.Font(family='Helvetica', size=24, weight = "bold") # Font settings

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
