import numpy as np
import cutils
import math

Kp = 1.0        #speed proportional gain
Ki = 0.05       
Kd = 0.01

k = 0.1         #look forward gain
Lfc = 2.0       #look-ahead distance
L = 2.85

INTERP_LOOKAHEAD_DISTANCE = 20   # lookahead in meters
INTERP_DISTANCE_RES       = 0.01 # distance between interpolated points

ITER_FOR_SIM_TIMESTEP  = 10     # no. iterations to compute approx sim timestep
WAIT_TIME_BEFORE_START = 5.00   # game seconds (time before controller start)
TOTAL_RUN_TIME         = 200.00 # game seconds (total runtime before sim end)
TOTAL_FRAME_BUFFER     = 300    # number of frames to buffer after total runtime
NUM_PEDESTRIANS        = 0      # total number of pedestrians to spawn
NUM_VEHICLES           = 0      # total number of vehicles to spawn
SEED_PEDESTRIANS       = 0      # seed for pedestrian spawn randomizer
SEED_VEHICLES          = 0      # seed for vehicle spawn randomizers

WAYPOINTS_FILENAME = 'racetrack_waypoints.txt'
DIST_THRESHOLD_TO_LAST_WAYPOINT = 2.0

class Controller2D(object):
    def __init__(self, waypoints):
        self.vars                = cutils.CUtils()
        self._current_x          = 0
        self._current_y          = 0
        self._current_yaw        = 0
        self._current_speed      = 0
        self._desired_speed      = 0
        self._current_frame      = 0
        self._current_timestamp  = 0.0
        self._start_control_loop = False
        self._set_throttle       = 0
        self._set_brake          = 0
        self._set_steer          = 0
        self._waypoints          = waypoints
        self._conv_rad_to_steer  = 180.0 / 70.0 / np.pi
        self._pi                 = np.pi
        self._2pi                = 2.0 * np.pi
        self.minusonex = 0
        self.zerox = 0

    def update_values(self, x, y, zerox ,minusonex, yaw, speed, timestamp, frame):
        self._current_x         = x
        self._current_y         = y
        self.minusonex = minusonex
        self.zerox = zerox 
        self._current_yaw       = yaw
        self._current_speed     = speed
        self._current_timestamp = timestamp
        self._current_frame     = frame
        if self._current_frame:
            self._start_control_loop = True

    def update_desired_speed(self):
        min_idx       = 0
        min_dist      = float("inf")
        desired_speed = 0
        for i in range(len(self._waypoints)):
            dist = np.linalg.norm(np.array([
                    self._waypoints[i][0] - self._current_x,
                    self._waypoints[i][1] - self._current_y]))
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        if min_idx < len(self._waypoints)-1:
            desired_speed = self._waypoints[min_idx][2]
        else:
            desired_speed = self._waypoints[-1][2]
        self._desired_speed = desired_speed

    def update_waypoints(self, new_waypoints):
        self._waypoints = new_waypoints

    def get_commands(self):
        return self._set_throttle, self._set_steer, self._set_brake

    def set_throttle(self, input_throttle):
        # Clamp the throttle command to valid bounds
        throttle           = np.fmax(np.fmin(input_throttle, 1.0), 0.0)
        self._set_throttle = throttle

    def set_steer(self, input_steer_in_rad):
        # Covnert radians to [-1, 1]
        input_steer = self._conv_rad_to_steer * input_steer_in_rad

        # Clamp the steering command to valid bounds
        steer           = np.fmax(np.fmin(input_steer, 1.0), -1.0)
        self._set_steer = steer

    def set_brake(self, input_brake):
        # Clamp the steering command to valid bounds
        brake           = np.fmax(np.fmin(input_brake, 1.0), 0.0)
        self._set_brake = brake

    def update_controls(self):
        x               = self._current_x
        y               = self._current_y
        yaw             = self._current_yaw
        v               = self._current_speed
        self.update_desired_speed()
        v_desired       = self._desired_speed
        t               = self._current_timestamp
        waypoints       = self._waypoints
        throttle_output = 0
        steer_output    = 0
        brake_output    = 0
        v_magnitude = math.sqrt(v.x**2 + v.y**2)

        self.vars.create_var('v_previous', 0.0)
       
        frame = 0


        # Skip the first frame to store previous values properly
        if self._start_control_loop:
            a = Kp * (v_desired - v_magnitude)

            throttle_output = min(1.0, max(0.0, (a * t + throttle_output)/2))
            brake_output    = 0

            length = np.arange(0,100,1)
            dx = [self._current_x - waypoints[icx][0] for icx in length]
            dy = [self._current_y - waypoints[icy][1] for icy in length]
            d = [abs(math.sqrt(idx ** 2 + idy ** 2)) for (idx,idy) in zip(dx,dy)]
            ind = d.index(min(d))
            if ind < 2:
                tx = waypoints[ind][0]
                ty = waypoints[ind][1]  
            else:
                tx = self.minusonex[0]
                ty = self.minusonex[1]

            alpha_hat = math.atan2(ty - y,tx - x)
            alpha = alpha_hat - yaw
            Lf = k * v_magnitude + Lfc
            steer_output = math.atan2(2.0 * L * math.sin(alpha) / Lf, 1.0)
            if steer_output > np.pi:
                steer_output -= 2 * np.pi
            if steer_output < - np.pi:
                steer_output += 2 * np.pi
            steer_output = np.clip(steer_output, -1.22, 1.22)

            self.set_throttle(throttle_output)  # in percent (0 to 1)
            self.set_steer(steer_output)        # in rad (-1.22 to 1.22)
            self.set_brake(brake_output)        # in percent (0 to 1)

            frame += 1

        self.vars.v_previous = v 