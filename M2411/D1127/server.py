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
        self.frame = 0
        data = self.json_formatting(0, 0, 0, "INIT")
        self.socket.send(data)

    def run(self, ):
        print(f'>> Connected by :{self.vehicle_id}')
        time.sleep(3)

        while True:
            try:
                if self.front == self.vehicle_id:
                    self.flag = True
                    thread = threading.Thread(target=self.leader_vehicle_waypoint_sending_func, args=(), daemon=True)
                    thread.start()
                    
                data = self.socket.recv(1024).decode('utf-8')
                data = self.json_parsing()
                print(f'>> Received from {self.vehicle_id} : ', data["PROTOCOL"])

                if not data:
                    print(f'>> Disconnected by {self.vehicle_id}')
                    break

                if data["PROTOCOL"] == "탈출":
                    for i in range(len(vehicles)):
                        if vehicles[i]["VEHICLE_ID"] == self.front:
                            vehicles[i]["REAR"] = vehicles[i]["VEHICLE_ID"]
                            vehicles[i]["SOCKET"].send(data)
                        self.front = self.vehicle_id

                elif data["PROTOCOL"] == "합류":
                    self.front = data["FRONT"]
                    for i in range(len(vehicles)):
                        if vehicles[i]["VEHICLE_ID"] == self.front:
                            vehicles[i]["REAR"] = self.vehicle_id
                            vehicles[i]["SOCKEt"].send(data)
                            
                else:
                    data = self.json_formatting(data["X"], data["Y"], data["SPEED"], data["PROTOCOL"])
                    for vehicle in vehicles:
                        if vehicle.vehicle_id == self.rear:
                            vehicle.socket.send(data)

            except ConnectionResetError as e:
                print(f'>> Disconnected by {self.vehicle_id}')
                break    

        
        vehicles.remove(self)
        self.socket.close()

    def leader_vehicle_waypoint_sending_func(self, ):
        while self.frame < len(waypoints) and self.flag:
            xys = waypoints_np[self.frame:self.frame+1]
            x, y, s = xys

            data = self.json_formatting(x,y,s, "SEND_DATA")
            for vehicle in vehicles:
                if vehicle.vehicle_id == self.front:
                    vehicle.socket.send(data)
            self.frame += 1

            if not self.flag:
                break
        
    ##### JSON FORMATTING, PARSING #####

    def json_formatting(self, x, y, speed, protocol):
        data = {"X" : x, 
                "Y" : y, 
                "SPEED" : speed, 
                "FRAME" : self.frame,
                "FRONT" : self.front,
                "VEHICLE_ID" : self.vehicle_id,
                "REAR" : self.rear,
                "PROTOCOL" : protocol,}
        data = json.dumps(data).encode('UTF-8')
        return data

    def json_parsing(self, data):
        data = json.load(data.decode())
        self.frame = data["FRAME"]
        self.front = data["FRONT"]
        self.rear = data["REAR"]
        return data

def main():
    
    server_socket = server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 1234))
    server_socket.listen()

    global vehicles 
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
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], vehicles[1].vehicle_id, data["VEHICLE_ID"])
                vehicles.append(vehicle)
            
            vehicle.daemon()
            vehicle.start()

    except Exception as e:
        print('에러 : ', e)

    finally:
        vehicle.join()


if __name__ == '__main__':

    main()