import socket
from _thread import *

 # Waypoints 관련 Import
import csv
import numpy as np

client_sockets = {}
client_socket_platoons = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 1234))
server_socket.listen()

WAYPOINTS_FILENAME = 'racetrack_waypoints.txt'

waypoints_file = WAYPOINTS_FILENAME
with open(waypoints_file) as waypoints_file_handle:
    waypoints = list(csv.reader(waypoints_file_handle, delimiter=',', quoting=csv.QUOTE_NONNUMERIC))
waypoints_np = np.array(waypoints)

def threaded(client_socket, addr):
    global client_socket_platoons

    frame = 0

    print('>> Connected by :', addr[0], ':', addr[1])
    ## process until client disconnect ##
    while True:
        try:
            if client_socket['first'][0] == client_socket:
                data = waypoints_np[frame]
                data = f"{frame}:{data}"
                client_sockets['first'][0].send(data.encode())
                frame += 1
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024).decode('utf-8')
            
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                if client_sockets['first'][0] == client_socket:
                    try:
                        client_sockets['first'] = client_sockets['second'].values()
                        client_sockets['second'] = client_sockets['third']
                        client_sockets.pop('third')
                    except:
                        pass
                elif client_sockets['second'][0] == client_socket:
                    try:
                        client_sockets['second'] = client_sockets['third']
                        client_sockets.pop(3)
                    except:
                        pass
                elif client_sockets['third'][0] == client_socket:
                    client_sockets.pop(3)
                else:
                    pass
                break

            print('>> Received from ' + addr[0], ':', addr[1], data)

            ## chat to client connecting client ##
            ## chat to client connecting client except person sending message ##
            if len(client_sockets) > 2:
                if client_sockets['first'][0] == client_socket:
                    data = f"{client_sockets['first'][1]}:{data}"
                    print(data)
                    client_sockets['second'][0].send(data.encode())
                elif client_sockets['second'][0] == client_socket:
                    data = f"{client_sockets['second'][1]}:{data}"
                    print(data)
                    client_sockets['third'][0].send(data.encode())
                else:
                    pass
            
        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break
    
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()



try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()

        data = client_socket.recv(1024).decode('utf-8')
        id, c_id = data.split(",")
        c_id = int(c_id)
        client_sockets[id] = [client_socket, c_id]
        start_new_thread(threaded, (client_socket, addr))
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()

