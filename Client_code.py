import socket
import threading
import tkinter as tk
from tkinter import *
import tkinter.simpledialog

base = tk.Tk()
base.title("Chatbox")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

mess = ""
count = 0

def view(msg):
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END,msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

def sendd():
    global count
    global mess
    msg = EntryBox.get("1.0",'end-1c').strip()
    nick = msg
    EntryBox.delete("0.0",END)
    mess = msg
    count += 1
    return nick

SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= sendd )

EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))

name = tkinter.simpledialog.askstring("Name", "Choose your name?")
nickname = name


def receive():
    while True:
        try:
            message = client.recv(1024). decode('ascii')
            if message=='NICK':
                client.send(nickname.encode('ascii'))
            else:
                view(message)
        except:
            print ("An error occurred")
            client.close()
            break

def write():
    global count
    while True:
        if count > 0:
            message = f'{nickname}: {mess}'
            client.send(message.encode('ascii'))
            count -= 1

receive_thread =  threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread (target=write)
write_thread.start()

base.mainloop()
