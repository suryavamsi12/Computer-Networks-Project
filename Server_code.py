'''import tkinter
from tkinter import *

base = Tk()
base.title("Hello")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set





#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
base.mainloop()
'''
import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket (socket.AF_INET, socket. SOCK_STREAM)
server.bind ((host, port))
server.listen()

clients = []
nicknames = []

def broadcast (message):
    for client in clients:
        client.send(message)

def handle(client) :
    while True:
        try:
            message = client.recv(1024)
            broadcast (message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast (f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove (nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f" Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append (nickname)
        clients.append (client)

        print(f"Nickname of the client is {nickname}")
        broadcast (f' {nickname} joined the chat'.encode('ascii'))        
        thread = threading. Thread(target=handle, args=(client,))
        thread.start()

print('the server is listening')
receive()
