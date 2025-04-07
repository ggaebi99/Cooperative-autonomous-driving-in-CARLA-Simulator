import socket
import threading

 # Waypoints 관련 Import
import csv
import numpy as np
import json

import time

WAYPOINTS_FILENAME = 'racetrack_waypoints.txt'

waypoints_file = WAYPOINTS_FILENAME
with open(waypoints_file) as waypoints_file_handle:
    waypoints = list(csv.reader(waypoints_file_handle, delimiter=',', quoting=csv.QUOTE_NONNUMERIC))
waypoints_np = np.array(waypoints)



##### VEHICLE SOCKET CLASS #####

class VehicleSocket(threading.Thread):
    def __init__(self, socket, vehicle_id, front, rear) -> None:
        self.vehicle_id = vehicle_id
        self.socket = socket
        self.front  = front
        self.rear = rear
        self.flag = False

    def run(self):
        pass

    def leader_vehicle_waypoint_sending_func(self, vehicle, frame, ):
        while frame < len(waypoints):
            xys = waypoints_np[frame:frame+1]
            x, y, s = data

            data = self.json_formatting(x,y,s,frame,vehicle["FRONT"], vehicle["REAR"], "SEND_DATA")
            vehicle["SOCKET"].send()
            
            frame += 1

    ##### JSON FORMATTING, PARSING #####

    def json_formatting(self, x, y, speed, frame, protocol):
        data = {"X" : x, 
                "Y" : y, 
                "SPEED" : speed, 
                "FRAME" : self.frame,
                "FRONT" : self.front,
                "VEHICLE_ID" : self.palyer.id,
                "REAR" : self.rear,
                "PROTOCOL" : protocol,}
        data = json.dumps(data).encode('UTF-8')
        return data

    def json_parsing(data):
        data = json.load(data.decode())
        return data







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
    print(f'>> Connected by :{platoons[pla_num][oov]["vehicle_id"]}')
    time.sleep(3)
    ## process until client disconnect ##
    while True:
        try:
            if platoons[pla_num][oov]["vehicle_id"] == platoons[pla_num][oov]["front"] and platoons[pla_num][oov]["flag"] == False:
                platoons[pla_num][oov]["flag"] = True 
                self.start_new_thread(self.first_send_thread, (client_socket, frame))
            
            ## send client if data recieved(echo) ##
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f'>> Disconnected by {platoons[pla_num][oov]["vehicle_id"]}')
                break
            if data == "front":
                platoons[pla_num][oov-1]["rear"] = platoons[pla_num][oov-1]["vehicle_id"]
                platoons[pla_num][oov]["front"] = platoons[pla_num][oov]["vehicle_id"]
                continue
            elif data == "rear":
                platoons[pla_num][oov]["front"] = platoons[pla_num][oov-1]["vehicle_id"]
                platoons[pla_num][oov-1]["rear"] = platoons[pla_num][oov]["vehicle_id"]
                platoons[pla_num][oov]["flag"] = False
                continue
            else:
                print(f'>> Received from {platoons[pla_num][oov]["vehicle_id"]}:', data)
                frame = int(data.split(",")[-1])

                
                if platoons[pla_num][oov]["vehicle_id"] == platoons[pla_num][oov]["rear"]:
                    continue

                data = f"{platoons[pla_num][oov]['vehicle_id']}:{platoons[pla_num][oov+1]['rear']}:{data}\n"
                for a in platoons:
                    for b in a:
                        if platoons[pla_num][oov]["rear"] == b["vehicle_id"]:
                            b["socket"].send(data.encode())
                            print(data)


                ## chat to client connecting client ##
                ## chat to client connecting client except person sending message ##
            
            
        except ConnectionResetError as e:
            print(f'>> Disconnected by {platoons[pla_num][oov]["vehicle_id"]}')
            break
    
    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()




def main():
    
    server_socket = server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 1234))
    server_socket.listen()

    vehicles = []

    try:
        while True:
            print('>> Wait')

            client_socket, addr = server_socket.accept()
            
            data = client_socket.recv(1024)
            data = json.load(data.decode())

            if data["x"] == 1:
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], data["VEHICLE_ID"], data["VEHICLE_ID"])
                vehicles.append(vehicle)
            elif data["x"] == 2:
                vehicles[0].rear = data["VEHICLE_ID"]
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], vehicles[0].vehicle_id, data["VEHICLE_ID"])
                vehicles.append(vehicle)
            elif data["x"] == 3:
                vehicles[1].rear = data["VEHICLE_ID"]
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], vehicles[0].vehicle_id, data["VEHICLE_ID"])
                vehicles.append(vehicle)
            
            vehicle.daemon()
            vehicle.start()

    except Exception as e:
        print('에러 : ', e)

    finally:
        server_socket.close()


if __name__ == '__main__':

    main()