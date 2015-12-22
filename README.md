# Simulation-of-Server-and-Client-Connection-for-Data-Streaming
python-twisted library

we have used twisted library and python programming language. Twisted is an event-driven networking engine written in Python. The goal was to use TCP and UDP protocols to implement a server that controls data streaming between some clients. Each client by establishing a TCP connection with server and registering in server’s clients list, will have the authority to send and receive data. Any client that gets confirmation from sever after it’s request, can establish a UDP connection for sending it’s data. After that, other clients will be asked if they want to receive data or not. Server will make a chain connection between sender client and receivers. Data will be passed to according clients.
