# Computer-Networks-Project

We have implemented a Chat Room wherein you can participate in the group chat with connected clients as well as send private messages to a particular client.
We use Socket Programming and Multi-threading for implementing this. TCP socket has been used as it garuantees reliable data delivery i.e. no information will be lost.

The server code is responsible for regulating the communication between clients. Each client sends a connection request to the server. Everytime a new client connected a new thread is created for that client. The client code initialization the connection request. It is responsible for checking messages incoming from the server as well as checking if the user wants to send a message to the server.

Each user has to run the client code separately after the server code is running. Once the client connects to the server, the client receives a message from the server asking for nickname ("NICK"), the client then has to send its nickname back to the server. All the communication is done using the nickname mentioned by the client.
