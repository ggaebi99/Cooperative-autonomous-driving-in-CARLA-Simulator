import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree

way_point_text = open("racetrack_waypoints.txt", "r")
first_text = open("first_50.txt", "r")
second_25_text = open("second_25.txt", "r")
second_50_text = open("second_50.txt", "r")
second_75_text = open("second_75.txt", "r")
second_100_text = open("second_100.txt", "r")

w = way_point_text.readlines()
f = first_text.readlines()
s_25 = second_25_text.readlines()
s_50 = second_50_text.readlines()
s_75 = second_75_text.readlines()
s_100 = second_100_text.readlines()


w_x = []
w_y = []

for i in w:
    a = i.replace("\n", "").replace(" ", "").split(",")
    w_x.append(float(a[0]))
    w_y.append(float(a[1]))

f_x = []
f_y = []

for i in f:
    a = i.replace("\n", "").replace(" ", "").replace("X","").replace("Y","").replace(":","").split(",")
    print(a)
    f_x.append(float(a[0]))
    f_y.append(float(a[1]))

s_25_x = []
s_25_y = []

s_50_x = []
s_50_y = []

s_75_x = []
s_75_y = []

s_100_x = []
s_100_y = []

for i in s_25:
    a = i.replace("\n", "").replace(" ", "").replace("X","").replace("Y","").replace(":","").split(",")
    s_25_x.append(float(a[0]))
    s_25_y.append(float(a[1]))

for i in s_50:
    a = i.replace("\n", "").replace(" ", "").replace("X","").replace("Y","").replace(":","").split(",")
    s_50_x.append(float(a[0]))
    s_50_y.append(float(a[1]))
    
for i in s_75:
    a = i.replace("\n", "").replace(" ", "").replace("X","").replace("Y","").replace(":","").split(",")
    s_75_x.append(float(a[0]))
    s_75_y.append(float(a[1]))

for i in s_100:
    a = i.replace("\n", "").replace(" ", "").replace("X","").replace("Y","").replace(":","").split(",")
    s_100_x.append(float(a[0]))
    s_100_y.append(float(a[1]))

# # 최소 거리 계산 함수
# def calculate_min_distances(points_x, points_y, waypoints_x, waypoints_y):
#     distances = []
#     for px, py in zip(points_x, points_y):
#         min_distance = float('inf')  # 초기값을 무한대로 설정
#         for wx, wy in zip(waypoints_x, waypoints_y):
#             distance = np.sqrt((px - wx) ** 2 + (py - wy) ** 2)
#             if distance < min_distance:
#                 min_distance = distance
#         distances.append(min_distance)
#     return distances

# # First와 Second 최소 거리 계산
# first_distances = calculate_min_distances(f_x, f_y, w_x, w_y)
# second_distances = calculate_min_distances(s_x, s_y, w_x, w_y)

# # 오차 시각화
# plt.figure(figsize=(10, 6))

# plt.plot(range(len(first_distances)), first_distances, label="First 50 Errors", marker="o", linestyle="--", alpha=0.1)
# plt.plot(range(len(second_distances)), second_distances, label="Second 50 Errors", marker="s", linestyle="--", alpha=0.1)

# plt.xlabel("Point Index")
# plt.ylabel("Error (Minimum Distance to Waypoints)")
# plt.title("Error Comparison between First 50 and Second 50")
# plt.legend()
# plt.grid(True)

# plt.show()



# Waypoints KDTree 생성
waypoints_tree = KDTree(np.column_stack((w_x, w_y)))
waypoints_tree_f = KDTree(np.column_stack((f_x, f_y)))

# First와 Second 각각의 최소 거리 계산
first_points = np.column_stack((f_x, f_y))
second_25_points = np.column_stack((s_25_x, s_25_y))
second_50_points = np.column_stack((s_50_x, s_50_y))
second_75_points = np.column_stack((s_75_x, s_75_y))
second_100_points = np.column_stack((s_100_x, s_100_y))

first_distances, _ = waypoints_tree.query(first_points)
second_25_distances, _ = waypoints_tree.query(second_25_points)
second_50_distances, _ = waypoints_tree.query(second_50_points)
second_75_distances, _ = waypoints_tree.query(second_75_points)
second_100_distances, _ = waypoints_tree.query(second_100_points)

# 오차 시각화
plt.figure(figsize=(10, 6))

plt.plot(range(len(first_distances)), first_distances, label="First 50 Errors", marker="o", linestyle="--", alpha=0.2)
plt.plot(range(len(second_25_distances)), second_25_distances, label="Second 25 Errors", marker="s", linestyle="--", alpha=0.2)
plt.plot(range(len(second_50_distances)), second_50_distances, label="Second 50 Errors", marker="s", linestyle="--", alpha=0.2)
plt.plot(range(len(second_75_distances)), second_75_distances, label="Second 75 Errors", marker="s", linestyle="--", alpha=0.2)
plt.plot(range(len(second_100_distances)), second_100_distances, label="Second 100 Errors", marker="s", linestyle="--", alpha=0.2)

plt.xlabel("Point Index")
plt.ylabel("Error (Minimum Distance to Waypoints)")
plt.title("Error Comparison between First 50 and Second 50")
plt.legend()
plt.grid(True)

plt.show()

# 통계량 출력
print(f"First 50 - Mean Error: {np.mean(first_distances):.4f}, Max Error: {np.max(first_distances):.4f}")
print(f"Second 25 - Mean Error: {np.mean(second_25_distances):.4f}, Max Error: {np.max(second_25_distances):.4f}")
print(f"Second 50 - Mean Error: {np.mean(second_50_distances):.4f}, Max Error: {np.max(second_50_distances):.4f}")
print(f"Second 75 - Mean Error: {np.mean(second_75_distances):.4f}, Max Error: {np.max(second_75_distances):.4f}")
print(f"Second 100 - Mean Error: {np.mean(second_100_distances):.4f}, Max Error: {np.max(second_100_distances):.4f}")



second_25_distances_f, _ = waypoints_tree_f.query(second_25_points)
second_50_distances_f, _ = waypoints_tree_f.query(second_50_points)
second_75_distances_f, _ = waypoints_tree_f.query(second_75_points)
second_100_distances_f, _ = waypoints_tree_f.query(second_100_points)

plt.figure(figsize=(10, 6))

plt.plot(range(len(second_25_distances)), second_25_distances_f, label="Second 25 Errors", marker="*", linestyle="--", alpha=0.2)
plt.plot(range(len(second_50_distances)), second_50_distances_f, label="Second 50 Errors", marker="s", linestyle="--", alpha=0.2)
plt.plot(range(len(second_75_distances)), second_75_distances_f, label="Second 75 Errors", marker="H", linestyle="--", alpha=0.2)
plt.plot(range(len(second_100_distances)), second_100_distances_f, label="Second 100 Errors", marker="^", linestyle="--", alpha=0.2)

plt.xlabel("Point Index")
plt.ylabel("Error (Minimum Distance to Waypoints)")
plt.title("Error Comparison between waypoints and TSB")
plt.legend()
plt.grid(True)

plt.show()

# 통계량 출력
print(f"Second 25 - Mean Error: {np.mean(second_25_distances_f):.4f}, Max Error: {np.max(second_25_distances_f):.4f}")
print(f"Second 50 - Mean Error: {np.mean(second_50_distances_f):.4f}, Max Error: {np.max(second_50_distances_f):.4f}")
print(f"Second 75 - Mean Error: {np.mean(second_75_distances_f):.4f}, Max Error: {np.max(second_75_distances_f):.4f}")
print(f"Second 100 - Mean Error: {np.mean(second_100_distances_f):.4f}, Max Error: {np.max(second_100_distances_f):.4f}")