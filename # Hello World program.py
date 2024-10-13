import sys

import struct
#This module helps you convert between Python values and C structs represented as Python 
# bytes objects.It can be useful if you want to unpack binary data according to a specific format.

import os
#If you want to work with file paths, check if files exist, or manipulate directories, the os module is very helpful.
#python

#import numpy
#If you want to perform more complex 
#numerical operations on binary data, numpy is a powerful library.

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
#Tkinter gui 

import hexdump
#tool for hex dumping in readable format




#def offset():










#gets the /.../...// from user
def import_data():
    try:
       # file_path = filedialog.askopenfilename(title="Select .sav file", filetypes=[("Save files", "*.sav")])
        file_path = r"C:\Users\AdamA\Desktop\Future Goals\Pokemon\AAAAAAA VS CCCCCCC.sav"  # Change 'your_file.sav' to your actual file name

        if not file_path: 
            messagebox.showerror("NO FILE SELECTED")
            return 
            
        #Use with so it cloes automatically 
        with open(file_path, "rb") as file:
            data = file.read()

        #Use return to store it in data_16
        data_16  = hexdump.hexdump(data, result='return')

    except:
        messagebox.showerror("ERROR")    



    #Split the data_16 into a list using split line.
    lines = data_16.splitlines()
    #00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
   

    offset = []
    byte_data = []
    decoded_text  = []


    for x in range(len(lines)):
        offset.append(str(lines[x])[:10])
        byte_data.append(str(lines[x])[10:58])
        decoded_text.append(str(lines[x])[58:])
     #   print(offset[x])
       # print(byte_data[x])
      #  print(decoded_text[x])

        table.insert(parent = "", index ="end", values = (offset[x], byte_data[x], decoded_text[x]))
      #  print(len(byte_data))


## Convert the string data_16 into 3 sections: 
# 1. offset 
# 2. Data 
# 3. Decoded test






window = tk.Tk()
window.title("Pokemon Editor")
window.geometry("800x600")

#Create widgets

label = ttk.Label(master = window, text = "Hex Editor")
#adds some space 
label.pack(pady =10)

#button
button=ttk.Button(master = window, text = "Import Data", command = import_data )
button.pack(pady =10)

#Table
table = ttk.Treeview(window, columns = ("Offset", "Data", "Decoded Text"), show="headings")
table.heading("Offset", text= "Offset (h)")
table.heading("Data", text= "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
table.heading("Decoded Text", text= "Decoded Text")

table.pack()




#offset_label = ttk.Label(master = window, text = "Offset", foreground="blue")
#label.pack(pady =10)


#Text box. Pack is in the middle at the tops






#Run
window.mainloop()