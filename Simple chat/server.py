import socket
import base64
import hashlib
from Cryptodome.Cipher import AES as domeAES
from Cryptodome.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES as cryptoAES

BLOCK_SIZE = cryptoAES.block_size

key = "A%D*G-KaPdSgVkYp".encode()
__key__ = hashlib.sha256(key).digest()


def encrypt(raw):
    BS = cryptoAES.block_size  # get fixed block size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(cryptoAES.block_size)
    cipher = cryptoAES.new(key=__key__, mode=cryptoAES.MODE_CFB, iv=iv)
    a = base64.b64encode(iv + cipher.encrypt(raw))
    IV = Random.new().read(BLOCK_SIZE)
    aes = domeAES.new(__key__, domeAES.MODE_CFB, IV)
    b = base64.b64encode(IV + aes.encrypt(a))
    return b


def decrypt(enc):
    passphrase = __key__
    encrypted = base64.b64decode(enc)
    IV = encrypted[:BLOCK_SIZE]
    aes = domeAES.new(passphrase, domeAES.MODE_CFB, IV)
    enc = aes.decrypt(encrypted[BLOCK_SIZE:])
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:cryptoAES.block_size]
    cipher = cryptoAES.new(__key__, cryptoAES.MODE_CFB, iv)
    b = unpad(base64.b64decode(cipher.decrypt(enc[cryptoAES.block_size:])).decode('utf8'))
    return b


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1234
ADDR = SERVER, PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen()
print('Server is listening...')
c, adr = s.accept()


def chat():
    print(f'Connected from {adr}')
    connected = True
    while connected:
        msg = c.recv(1024)
        if msg == 'quit':
            connected = False
            s.close()
            print('Server closed')
        else:
            print(decrypt(msg))
        c.send(encrypt(input('SERVER: ')))


chat()
