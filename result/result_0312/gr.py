import numpy as np
import matplotlib.pyplot as plt

# 파일 읽기
with open('second.txt', 'r') as file:
    lines = file.readlines()

# 좌표 파싱
def parse_coordinates(data):
    x_coords, y_coords = [], []
    for line in data:
        parts = line.replace('\n', '').replace(' ', '').replace('X', '').replace('Y', '').replace(':', '').split(',')
        if len(parts) >= 2:
            x_coords.append(float(parts[0]))
            y_coords.append(float(parts[1]))
    return np.array(x_coords), np.array(y_coords)

x_coords, y_coords = parse_coordinates(lines)

# 선형 보간 함수
def interpolate_path(x, y, step=0.5):
    interpolated_x, interpolated_y = [x[0]], [y[0]]
    
    for i in range(1, len(x)):
        distance = np.hypot(x[i] - x[i-1], y[i] - y[i-1])
        num_points = int(distance // step)

        for j in range(1, num_points + 1):
            interp_x = x[i-1] + (x[i] - x[i-1]) * (j / num_points)
            interp_y = y[i-1] + (y[i] - y[i-1]) * (j / num_points)
            interpolated_x.append(interp_x)
            interpolated_y.append(interp_y)
        
        interpolated_x.append(x[i])
        interpolated_y.append(y[i])

    return np.array(interpolated_x), np.array(interpolated_y)

# 경로 보간
smooth_x, smooth_y = interpolate_path(x_coords, y_coords, step=0.1)

# 결과 시각화
plt.figure(figsize=(10, 6))
# plt.plot(x_coords, y_coords, 'o-', label='Original Path', alpha=0.5)
# plt.plot(smooth_x, smooth_y, 'r-', label='Interpolated Path', alpha=0.8)
plt.plot(smooth_x, smooth_y, 'r-', label='Waypoints Path', alpha=0.8)
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Waypoints Path Visualization')
# plt.title('Path Smoothing via Interpolation')
plt.legend()
plt.grid(True)
plt.show()

# 보간된 경로 저장
with open('interpolated_first.txt', 'w') as outfile:
    for x, y in zip(smooth_x, smooth_y):
        outfile.write(f"X: {x}, Y: {y}\n")
