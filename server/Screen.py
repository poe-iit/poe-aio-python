##import tkinter as tk
##
##counter = 0
##stop = False
##
##def stopit():
##    global stop
##    print("stop", stop)
##    stop = True
##
##def counter_label(label):
##    global counter, stop
##    counter = 0
##    stop = False
##    print("start")
##    def count():
##        global counter, stop
##        counter += 1
##        label.config(text=str(counter))
##        if not stop:
##            label.after(1000, count)
##        print(stop)
##    count()
## 
##root = tk.Tk()
##root.title("Counting Seconds")
##label = tk.Label(root, fg="dark green")
##label.pack()
##counter_label(label)
##button = tk.Button(root, text='Stop', width=25, command = stopit)
##button.pack()
##
##root.mainloop()

import tkinter as tk

def test(c):
    msg = tk.Tk()
    label = tk.Label(msg, text = c)
    label.pack(side = "top", fill = "x", pady = 10)
    B1 = tk.Button(msg, text = "Okay", command = msg.destroy)
    B1.pack()
    msg.mainloop()

colours = ['red', 'green', 'orange', 'white']
labelList = ['Fire', 'Extreme Weather', 'Active shooter', 'Public Safety']
r = 0
root = tk.Tk()
for i in range(4):
    c = colours[i]
    l = labelList[i]
    tk.Button(root, text = l, width = 15, command = lambda l = l: test(l)).grid(row = r, column = 0)
    tk.Entry(bg = c, relief = tk.SUNKEN, width = 10).grid(row = r, column = 1)
    r += 1

root.mainloop()
