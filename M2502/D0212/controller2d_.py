import numpy as np
import cutils
import math
import carla

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

    def update_values(self, x, y, yaw, speed, timestamp, frame):
        self._current_x         = x
        self._current_y         = y
        self._current_yaw       = yaw
        self._current_speed     = speed
        self._current_timestamp = timestamp
        self._current_frame     = frame
        self.goggal_list = []
        if self._current_frame:
            self._start_control_loop = True
        # print("x : ", self._current_x)
        # print("y : ", self._current_y)

    def update_desired_speed(self):
        min_idx       = 0
        min_dist      = float("inf")
        desired_speed = 0
        for i in range(len(self._waypoints)):
            # print(self._waypoints)
            # print(self._current_x)
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
        # current_dist = np.linalg.norm(np.array([self._current_x, self._current_y]) - np.array(new_waypoints[0][:2]))
        # print("c_d", current_dist)
        # if current_dist >= DIST_THRESHOLD_TO_LAST_WAYPOINT:
        """
        for i in self.goggal_list:
            i.destory()
        """
        self._waypoints = new_waypoints
        """
        rsu_bp_1 = self.world.world.get_blueprint_library().find('static.prop.streetsign')
        for i in self._waypoints:
            spawn_point_rsu1 = carla.Transform(carla.Location(x=i[0], y=i[1], z=2), carla.Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000))
            rsu1 = self.world.world.spawn_actor(rsu_bp_1, spawn_point_rsu1)
            self.goggal_list.append(rsu1)
        """    
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
        # print(1)
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
        # print("v", v)
        v_magnitude = math.sqrt(v.x**2 + v.y**2)
        # print("b : ", v)

        self.vars.create_var('v_previous', 0.0)
        self.vars.create_var('t_last', 0.0)
        self.vars.create_var('E', 0.0)
        self.vars.create_var('e_previous', 0.0)
        Kp = 1
        Ki = 1
        Kd = 0.01
        # print(f"Current Frame: {self._current_frame}, Timestamp: {self._current_timestamp}")


        # Skip the first frame to store previous values properly
        if self._start_control_loop:
            # a = Kp * (v_desired - v_magnitude)
            # print("v_desired = ", v_desired)
            # print("a = ", a)
            # print("t = ", t)

            throttle_output = 0 #min(0.75, max(0.0, a * t + throttle_output))
            brake_output    = 0
            # i = 0
            # tx = waypoints[-1][0]
            # ty = waypoints[-1][1]
            # i += 1
            delta_t = t - self.vars.t_last
            e_current = v_desired - v_magnitude

            Proportional = Kp * e_current

            self.vars.E = self.vars.E + e_current * delta_t
            integral = Ki * self.vars.E

            if delta_t == 0:
                derivate = 0
            else:
                derivate = Kd * ((e_current - self.vars.e_previous)/delta_t)

            u = Proportional + integral + derivate    # u : input signal

            if u >= 0:
                throttle_output = min(u, 0.75)
                brake_output    = 0
            elif u < 0:
                throttle_output = 0
                brake_output    = -min(u, 0.75)

            steer_output = 0

            k = 0.5

            yaw_path = np.arctan2(waypoints[-1][1] - waypoints[0][1], waypoints[-1][0] - waypoints[0][0])
            yaw_diff = yaw_path - yaw
            # print("yaw_path", yaw_path)
            # print("yaw", yaw)
            if yaw_diff > np.pi:
                yaw_diff -= 2 * np.pi
            elif yaw_diff < -np.pi:
                yaw_diff += 2 * np.pi
            # print("yaw_diff", yaw_diff)

            slope = (waypoints[-1][1]-waypoints[0][1])/ (waypoints[-1][0]-waypoints[0][0])
            # print("0,0", self.zerox)
            # print("0,0", self.minusonex)
            # print("--", waypoints[-1])
            a = -slope
            b = 1.0
            c = (slope*waypoints[0][0]) - waypoints[0][1]

            crosstrack_error = (a*x + b*y + c) / np.sqrt(a**2 + b**2)

            yaw_cross_track = np.arctan2(y-waypoints[0][1], x-waypoints[0][0])
            # print("XXX : ", x)
            # print("YYY : ", y )
            yaw_path2ct = yaw_path - yaw_cross_track
            # print("yaw_cross_track", yaw_cross_track)
            if yaw_path2ct > np.pi:
                yaw_path2ct -= 2 * np.pi
            if yaw_path2ct < - np.pi:
                yaw_path2ct += 2 * np.pi
            if yaw_path2ct > 0:
                crosstrack_error = abs(crosstrack_error)

                yaw_diff_crosstrack = 0.0
            else:
                crosstrack_error = - abs(crosstrack_error)

                yaw_diff_crosstrack = np.arctan(k * crosstrack_error / (v_magnitude))
            
            # print(crosstrack_error, yaw_diff, yaw_diff_crosstrack)

            # 3. control low
            steer_expect = yaw_diff + yaw_diff_crosstrack
            # print("yaw_diff_crosstrack", yaw_diff_crosstrack)
            # print("steer_expect", steer_expect)
            if steer_expect > np.pi:
                steer_expect -= 2 * np.pi
            if steer_expect < - np.pi:
                steer_expect += 2 * np.pi
            steer_expect = min(1.22, steer_expect)
            steer_expect = max(-1.22, steer_expect)

            # 4. update
            steer_output = steer_expect

            self.set_throttle(0.3)  # in percent (0 to 1)
            #self.set_throttle(throttle_output)  # in percent (0 to 1)
            self.set_steer(steer_output)        # in rad (-1.22 to 1.22)
            self.set_brake(0)

            self.vars.v_previous = v_magnitude  # Store forward speed to be used in next step
            self.vars.t_last = t
            # print(1)

            
  
        #     length = np.arange(0,100,1)
        #     dx = [self._current_x - waypoints[icx][0] for icx in length]
        #     dy = [self._current_y - waypoints[icy][1] for icy in length]
        #     d = [abs(math.sqrt(idx ** 2 + idy ** 2)) for (idx,idy) in zip(dx,dy)]
        #     ind = d.index(min(d))
        #     if ind < 2:
        #         tx = waypoints[ind][0]
        #         ty = waypoints[ind][1]  
        #     else:
        #         tx = waypoints[-1][0]
        #         ty = waypoints[-1][1]
        #         # ind = self._current_x - 1    s

        #     alpha_hat = math.atan2(ty - y,tx - x)
        #     alpha = alpha_hat - yaw
        #     Lf = k * v_magnitude + Lfc
        #     steer_output = math.atan2(2.0 * L * math.sin(alpha) / Lf, 1.0)
        #     print(steer_output)
        #     steer_output = np.clip(steer_output, -1.0, 1.0)
        #     print("steer_output = ",steer_output)
        #     print("throttle_output = ", throttle_output)
        #     # print("Waypoints : ", self._waypoints)

        #     self.set_throttle(throttle_output)  # in percent (0 to 1)
        #     self.set_steer(steer_output)        # in rad (-1.22 to 1.22)
        #     self.set_brake(brake_output)        # in percent (0 to 1)

        # self.vars.v_previous = v  # Store forward speed to be used in next step