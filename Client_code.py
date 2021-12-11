import socket
import threading
import tkinter as tk
from tkinter import *
import tkinter.simpledialog
from PIL import ImageTk,Image
from tkinter import filedialog
import os
import urllib

# Creating GUI elements
base = tk.Tk()
base.title("Chatbox")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

ChatLog = Text(base, bd=0, bg="gray", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Global variables
mess = ""
count = 0
img_count = 0
img_dir = None

# function to view the message recieved from the server on the screen
def view(msg):
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END,msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

# Function that runs when "send msg" button is clicked (the text inside the entry box is copied to the global variable "mess")
def sendd():
    global count
    global mess
    msg = EntryBox.get("1.0",'end-1c').strip()    
    EntryBox.delete("0.0",END)
    mess = msg
    count += 1    

# code for handling "send Image" button (not working properly)
i = 0
imgToInsert = []
def add_image():
    global imgToInsert
    global nickname
    global count
    global i
    global img_count
    global img_dir
    mess = " "
    count += 1
    img=filedialog.askopenfilename(title = "Select your image",filetypes = [("Image Files",".png"),("Image Files",".jpg")])

    img_dir = img
    img_count += 1
        
    
    img = Image.open(img)
    img = img.resize((150, int(150*(img.size[1]/img.size[0]))), Image.ANTIALIAS)
    imgToInsert.append(ImageTk.PhotoImage(img))
    ChatLog.image_create(tk.END, image = imgToInsert[i])
    i = i+1
    view(" ")

# Some more GUI elements (buttons and text box to show the messages)
SendButton = Button(base, font=("Verdana",11,'bold'), text="Send msg", width="12", height=5,
                    bd=0, bg="black", activebackground="#3c9d9b",fg='#00ffff',
                    command= sendd )

image_send = Button(base, font=("Verdana",11,'bold'), bg ="#3c9d9b",  text = "Send Image", width = "12", height=2,command = add_image)

EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=45)
image_send.place(x=6, y=446, height = 45)

# take nickname from the user
name = tkinter.simpledialog.askstring("Name", "Choose your name?")
nickname = name

# connecting to the server
client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))



# code that runs in "receive_thread" (keeps looking for incoming messages and when recieves a message it shows the message on screen)
def receive():
    while True:
        try:
            message = client.recv(1024). decode('utf-8')
            if message=='NICK':
                client.send(nickname.encode('utf-8'))
            else:
                view(message)
        except:
            print ("An error occurred")
            client.close()
            break

# code that runs in "write_thread"
# takes the global variable "mess" and "count" when count > 0 which means
# that a new message is in the buffer (mess) and it has not been sent to the server
def write():
    global count
    global img_count
    while True:
        if count > 0:
            message = f'{nickname} : {mess}'
            client.send(message.encode('utf-8'))
            count -= 1
        if img_count > 0:
            file = open(img_dir, 'rb')
            image_data = file.read(1024)

            client.send("%%img_incoming%%".encode("utf-8"))
            while image_data:
                client.send(image_data)
                image_data = file.read(1024)                
            file.close()
            client.send("%%img_done%%".encode("utf-8"))            
            img_count -= 1

# creating the recieve and write threads
receive_thread =  threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread (target=write)
write_thread.start()

base.mainloop()
