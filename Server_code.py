import threading
import socket
import os
import urllib

# the IP address of host
host = '127.0.0.1'

# the port number
port = 55555

# here AF_INET is IPv4 and SOCK_STREAM is a TCP socket
server = socket.socket (socket.AF_INET, socket. SOCK_STREAM)

# it binds the server to the host IP address at the given port 
server.bind ((host, port))

# listens for the active connections
server.listen()

# list of clients
clients = []
# list of clients' nicknames
nicknames = []


# the function here broadcasts the message sent by the client, to the chat box of all other clients in the chat room
def broadcast (message):
    mess = message.decode('utf-8').split()                         # decodes and returns original message
    if mess[2] == "%%PM%%":                                        # for sending a PRIVATE MESSAGE to a client
        index = nicknames.index(mess[3])                           # determines which client sent a message and stores the nickname of the client
        client = clients[index]
        mess[2] = "(Private -> {}):".format(mess[3])               # sends a private message to the correct client
        print(mess[0])
        sender_index = nicknames.index(mess[0])
        sender_client = clients[sender_index]        
        mess.pop(3)
        client.send((" ".join(str(x) for x in mess)).encode('utf-8'))
        sender_client.send((" ".join(str(x) for x in mess)).encode('utf-8'))   # message is sent only to the mentioned client
        
    else:
        for client in clients:
            client.send(message)                                   # broadcasts the message to all other clients 



# code that runs in each client's thread
# the function here handles when client sends a message or when client leaves the chat/gets disconnected
def handle(client) :
    while True:
        try:
            message = client.recv(1024)                                        # socket attempts to receive data, in a buffer size of 1024 bytes at a time
            if message.decode("utf-8") == "%%img_incoming%%":                  # decodes information recieved and sends the original image      
                file = open('server_image.jpg', "wb")
                image_chunk = client.recv(1024)                                
                while image_chunk:                    
                    # if image_chunk.decode("utf-8") == "%%img_done%%":
                        # print("done")
                        # break
                    file.write(image_chunk)                    
                    image_chunk = client.recv(1024)

                file.close()
                print("file closed")
            else:
                broadcast (message)                                            # sends the message which is in text form
        except:
            index = clients.index(client)                                      # handles when client is disconnected or leaves the chat
            clients.remove(client)
            client.close()                                                     # closes client connection
            nickname = nicknames[index]
            broadcast (f'{nickname} left the chat'.encode('utf-8'))            # broadcasts the message that given client has left the chat
            nicknames.remove (nickname)                                        # removes client name from nicknames
            break

def receive():
    while True:
        client, address = server.accept()                                      # server accepts the connection request sent by client and stores the IP address
        print(f" Connected with {str(address)}")                               # connection formed with the client

        client.send("NICK".encode('utf-8'))                                    # asks the client for a nickname
        nickname = client.recv(1024).decode('utf-8')               
        nicknames.append (nickname)
        clients.append (client)                                                # receives, decodes and stores the nickname and the client

        print(f"Nickname of the client is {nickname}")                         # prints the nickname of client
        broadcast (f' {nickname} joined the chat'.encode('utf-8'))             # broadcasts the nickname of client
        thread = threading. Thread(target=handle, args=(client,))              # handles the thread for the client
        thread.start()

print('the server is listening')
receive()
