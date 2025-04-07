import socket
from _thread import *

 # Waypoints 관련 Import
import csv
import numpy as np

client_sockets = {}
platoons = [
    [  
        {"vehicle_id": 1, "socket": None, "front": 1, "rear" : 2, "flag" : False},
        {"vehicle_id": 2, "socket": None, "front": 1, 'rear' : 3, "flag" : False},
        {"vehicle_id": 3, "socket": None, "front": 2, 'rear' : 3, "flag" : False},
    ],
]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 1234))
server_socket.listen()

WAYPOINTS_FILENAME = 'racetrack_waypoints.txt'

waypoints_file = WAYPOINTS_FILENAME
with open(waypoints_file) as waypoints_file_handle:
    waypoints = list(csv.reader(waypoints_file_handle, delimiter=',', quoting=csv.QUOTE_NONNUMERIC))
waypoints_np = np.array(waypoints)


def first_send_thread(client_socket, frame):
    while frame < len(waypoints):
        for i in range(len(platoons)):
            for y in range(len(platoons[i])):
                if platoons[i][y]["socket"] == client_socket:
                    front = platoons[i][y]["vehicle_id"]
        data = waypoints_np[frame:frame+1]
        data = f"{front}:{data[0][0]},{data[0][1]},{data[0][2]},{frame}\n"
        client_socket.send(data.encode())
        frame += 1

def threaded(client_socket, addr):
    global platoons

    frame = 0

    pla_num = 0
    oov = 1

    for i in range(len(platoons)):
        for y in range(len(platoons[i])):
            if platoons[i][y]["socket"] == client_socket:
                pla_num = i
                oov = y
    print('>> Connected by :', addr[0], ':', addr[1])
    ## process until client disconnect ##
    while True:
        try:
            if platoons[pla_num][oov]["vehicle_id"] == platoons[pla_num][oov]["front"] and platoons[pla_num][oov]["flag"] == False:
                platoons[pla_num][oov]["flag"] = True 
                start_new_thread(first_send_thread, (client_socket, frame))
            
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            print('>> Received from ' + addr[0], ':', addr[1], data)
            frame = int(data.split(",")[-1])

            
            if platoons[pla_num][oov]["vehicle_id"] == platoons[pla_num][oov]["rear"]:
                continue
            data = f"{platoons[pla_num][oov]['vehicle_id']}:{data}\n"
            for a in platoons:
                for b in a:
                    if platoons[pla_num][oov]["rear"] == b["rear"]:
                        b["socket"].send(data.encode())
                        print(data)


            ## chat to client connecting client ##
            ## chat to client connecting client except person sending message ##
            
            
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
        if id == "first":
            platoons[0][0] = {"vehicle_id": c_id, "socket": client_socket, "front": c_id, "rear" : c_id, "flag" : False}
        elif id == "second":
            platoons[0][0]["rear"] = c_id
            platoons[0][1] = {"vehicle_id": c_id, "socket": client_socket, "front": platoons[0][0]["vehicle_id"], "rear" : c_id, "flag" : False}
        elif id == "third":
            platoons[0][1]["rear"] = c_id
            platoons[0][2] = {"vehicle_id": c_id, "socket": client_socket, "front": platoons[0][1]["vehicle_id"], "rear" : c_id, "flag" : False}
        start_new_thread(threaded, (client_socket, addr))
except Exception as e:
    print('에러 : ', e)

finally:
    server_socket.close()

