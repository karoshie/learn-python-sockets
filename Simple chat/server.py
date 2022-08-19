import socket


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = SERVER, PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR))

s.listen()
print('Server is listening...')
c, adr = s.accept()

def chat():
    
    connected = True
    while connected:
        print(f'Connected from {adr}')
        msg = c.recv(1024).decode('utf-8')
        if msg == 'quit':
            connected = False
            s.close()
            print('Server closed')
        else:
            print(msg)
        c.send(input('SERVER: ').encode('utf-8'))
    
chat()