import numpy as np
import cutils
import math

Kp = 1.0        #speed proportional gain
Ki = 0.05       
Kd = 0.01

k = 0.1         #look forward gain
Lfc = 2.0       #look-ahead distance
L = 2.85

class Controller2D(object):
    def __init__(self):
        self.vars                = cutils.CUtils()
        self._current_x          = 0
        self._current_y          = 0
        self._current_yaw        = 0
        self._current_speed      = 0
        self._desired_speed      = 0
        self._set_throttle       = 0
        self._set_brake          = 0
        self._set_steer          = 0
        self._waypoint          = None
        self._conv_rad_to_steer  = 180.0 / 70.0 / np.pi
        self._pi                 = np.pi
        self._2pi                = 2.0 * np.pi

    def update_values(self, x, y, yaw, speed):
        self._current_x         = x
        self._current_y         = y
        self._current_yaw       = yaw
        self._current_speed     = speed
        # print("x : ", self._current_x)
        # print("y : ", self._current_y)

    def update_desired_speed(self, desired_speed):
        self._desired_speed = desired_speed

    def update_waypoint(self, new_waypoint):
        self._waypoint = new_waypoint

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
        self.update_desired_speed(self._waypoint[2])
        v_desired       = self._desired_speed
        ## t               = self._current_timestamp
        waypoint       = self._waypoint
        throttle_output = 0
        steer_output    = 0
        brake_output    = 0
        v_magnitude = math.sqrt(v.x**2 + v.y**2)
        
        self.vars.create_var('v_previous', 0.0)


        # Skip the first frame to store previous values properly
        a = Kp * (v_desired - v_magnitude)

        throttle_output = min(1.0, max(0.0, (a + throttle_output)/2)) ## * t + throttle_output)/2))
        brake_output    = 0
        
        tx, ty = waypoint[:2] 

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

        self.vars.v_previous = v 