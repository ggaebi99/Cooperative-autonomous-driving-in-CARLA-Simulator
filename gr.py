import numpy as np
import pandas as pd
import scipy.interpolate as interp
import matplotlib.pyplot as plt

# Load the data
file_path = "racetrack_waypoints.txt"  # Replace with actual file path
data = np.loadtxt(file_path, delimiter=", ")

x, y, speed = data[:, 0], data[:, 1], data[:, 2]

# Create a finer interpolation using cubic splines
num_points = len(x) * 10  # Increase the number of points significantly
spline_t = np.linspace(0, 1, len(x))  # Normalize t values
interp_t = np.linspace(0, 1, num_points)

spline_x = interp.CubicSpline(spline_t, x)
spline_y = interp.CubicSpline(spline_t, y)
spline_speed = interp.CubicSpline(spline_t, speed)

x_interp = spline_x(interp_t)
y_interp = spline_y(interp_t)
speed_interp = spline_speed(interp_t)

# Save the interpolated data
interpolated_data = np.column_stack((x_interp, y_interp, speed_interp))
np.savetxt("interpolated_path.txt", interpolated_data, delimiter=", ", fmt="%.6f")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'bo-', markersize=3, label='Original Path')
plt.plot(x_interp, y_interp, 'r.', markersize=1, label='Interpolated Path')
plt.legend()
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Path Interpolation")
plt.show()