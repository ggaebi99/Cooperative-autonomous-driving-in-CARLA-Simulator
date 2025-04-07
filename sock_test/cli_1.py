import socket
from _thread import *

HOST = '127.0.0.1' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if data:
            print("recive : ", repr(data.decode()))

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

client_socket.send("1".encode())

while True:
    message = input()
    if message == 'quit':
        close_data = message
        break
    client_socket.send(message.encode())

client_socket.close()