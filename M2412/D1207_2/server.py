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

class VehicleSocket(threading.Thread, ):
    def __init__(self, socket, vehicle_id, front, rear):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.socket = socket
        self.front  = front
        self.rear = rear
        self.flag = False
        self.frame = 0
        data = self.json_formatting(0, 0, 0, self.frame, self.front, self.vehicle_id, self.rear, "INIT")
        self.socket.send(data)

    def run(self, ):
        print(f'>> Connected by :{self.vehicle_id}')

        time.sleep(3)        
        while True:
            try:
                if self.front == self.vehicle_id and self.flag == False:
                    self.flag = True
                    thread = threading.Thread(target=self.leader_vehicle_waypoint_sending_func, args=(self.frame,), daemon=True)
                    thread.start()
                    
                data = self.socket.recv(1024).decode('utf-8')
                data = self.json_parsing(data)
                if self.vehicle_id != self.rear:
                    print(f'>> Received from {self.vehicle_id} to', data["REAR"])

                if not data:
                    print(f'>> Disconnected by {self.vehicle_id}')
                    break

                if data["PROTOCOL"] == "탈출":
                    for i in range(len(vehicles)):
                        if vehicles[i].vehicle_id == self.front:
                            vehicles[i].rear = vehicles[i].vehicle_id
                            data = self.json_formatting(0,0,0,vehicles[i].frame, vehicles[i].front, vehicles[i].vehicle_id, vehicles[i].rear, "탈출")
                            vehicles[i].socket.send(data)
                    self.front = self.vehicle_id
                    print(f"\n탈출 {self.vehicle_id}, front : {self.front}, rear : {self.rear}\n")

                elif data["PROTOCOL"] == "합류":
                    self.front = data["FRONT"]
                    for i in range(len(vehicles)):
                        if vehicles[i].vehicle_id == self.front:
                            vehicles[i].rear = self.vehicle_id
                            data = self.json_formatting(0,0,0,vehicles[i].frame, vehicles[i].front, vehicles[i].vehicle_id, vehicles[i].rear, "합류")
                            vehicles[i].socket.send(data)
                    print(f"\n합류 {self.vehicle_id}, front : {self.front}, rear : {self.rear}\n")

                else:
                    for vehicle in vehicles:
                        if vehicle.vehicle_id == self.rear and self.vehicle_id != vehicle.vehicle_id:
                            data = self.json_formatting(data["X"], data["Y"], data["SPEED"], self.frame, vehicle.front, vehicle.vehicle_id, vehicle.rear, data["PROTOCOL"])
                            vehicle.socket.send(data)
                            

            except ConnectionResetError as e:
                print(f'>> Disconnected by {self.vehicle_id}')
                break    

        
        vehicles.remove(self)
        self.socket.close()

    def leader_vehicle_waypoint_sending_func(self, frame):
        while frame < len(waypoints) and self.flag:
            xys = waypoints_np[frame:frame+1]
            x, y, s = xys[0]
            data = self.json_formatting(x,y,s, frame, self.front, self.vehicle_id, self.rear, "SEND_DATA")

            for vehicle in vehicles:
                if vehicle.vehicle_id == self.front:
                    vehicle.socket.send(data)
            frame += 1
        
        
    ##### JSON FORMATTING, PARSING #####

    def json_formatting(self, x, y, speed, frame, front, vehicle_id, rear, protocol):
        data = {"X" : x, 
                "Y" : y, 
                "SPEED" : speed, 
                "FRAME" : frame,
                "FRONT" : front,
                "VEHICLE_ID" : vehicle_id,
                "REAR" : rear,
                "PROTOCOL" : protocol,}
        data = json.dumps(data).encode('utf-8')
        return data

    def json_parsing(self, data):
        data = json.loads(data)
        self.frame = data["FRAME"]
        self.front = data["FRONT"]
        self.rear = data["REAR"]
        return data

def temp_json_formatting(x, y, speed, frame, front, vehicle_id, rear, protocol):
    data = {"X" : x, 
            "Y" : y, 
            "SPEED" : speed, 
            "FRAME" : frame,
            "FRONT" : front,
            "VEHICLE_ID" : vehicle_id,
            "REAR" : rear,
            "PROTOCOL" : protocol,}
    data = json.dumps(data).encode('utf-8')
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
            data = json.loads(data.decode())
            if data["X"] == 1:
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], data["VEHICLE_ID"], data["VEHICLE_ID"])
                vehicles.append(vehicle)
            elif data["X"] == 2:
                vehicles[0].rear = data["VEHICLE_ID"]
                vehicles[0].socket.send(temp_json_formatting(0,0,0,0,vehicles[0].vehicle_id, vehicles[0].vehicle_id, data["VEHICLE_ID"], "INIT"))
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], vehicles[0].vehicle_id, data["VEHICLE_ID"])
                vehicles.append(vehicle)
            elif data["X"] == 3:
                vehicles[1].rear = data["VEHICLE_ID"]
                vehicles[1].socket.send(temp_json_formatting(0,0,0,0,vehicles[0].vehicle_id, vehicles[1].vehicle_id, data["VEHICLE_ID"], "INIT"))
                vehicle = VehicleSocket(client_socket, data["VEHICLE_ID"], vehicles[1].vehicle_id, data["VEHICLE_ID"])
                vehicles.append(vehicle)

            vehicle.start()

    except Exception as e:
        print('에러 : ', e)

    finally:
        vehicle.join()


if __name__ == '__main__':

    main()
