import socket
from _thread import *

client_sockets = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 1234))
server_socket.listen()

WAYPOINTS_FILENAME = 'racetrack_waypoints.txt'

def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])
    ## process until client disconnect ##
    while True:
        try:
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024).decode('utf-8')
            
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                if client_sockets[1][0] == client_socket:
                    try:
                        client_sockets[1] = client_sockets[2]
                        client_sockets[2] = client_sockets[3]
                        client_sockets.pop(3)
                    except:
                        pass
                elif client_sockets[2][0] == client_socket:
                    try:
                        client_sockets[2] = client_sockets[3]
                        client_sockets.pop(3)
                    except:
                        pass
                elif client_sockets[3][0] == client_socket:
                    client_sockets.pop(3)
                else:
                    pass
                break

            print('>> Received from ' + addr[0], ':', addr[1], data.decode('utf-8'))

            ## chat to client connecting client ##
            ## chat to client connecting client except person sending message ##
            if len(client_sockets) > 2:
                if client_sockets[1][0] == client_socket:
                    data = f"{client_sockets[2][1]}:{data}"
                    client_sockets[2][0].send(data.encode())
                elif client_sockets[2][0] == client_socket:
                    data = f"{client_sockets[2][1]}:{data}"
                    client_sockets[3][0].send(data.encode())
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

        id, c_id = client_socket.recv(1024).decode().split(",")
        id, c_id = int(id), int(c_id)
        client_sockets[id] = [client_socket, c_id]
        start_new_thread(threaded, (client_socket, addr))
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()

