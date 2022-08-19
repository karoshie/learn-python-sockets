import socket


CLIENT = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = CLIENT, PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user = input()

s.connect(ADDR)
connected = True
while connected:
    s.send(input(f'{user}: ').encode('utf-8'))
    msg = s.recv(1024).decode('utf-8')
    if msg == 'quit':
        connected = False
    else:
        print(msg)
