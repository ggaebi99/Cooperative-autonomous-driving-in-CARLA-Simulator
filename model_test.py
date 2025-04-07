import pandas as pd
import numpy as np

# 파일 경로 설정
file_path = "result/D0212/first.txt"

# 파일을 읽고 x, y 좌표 추출
coordinates = []
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        x = float(parts[0].split(':')[1].strip())
        y = float(parts[1].split(':')[1].strip())
        coordinates.append((x, y))

# DataFrame으로 변환
df = pd.DataFrame(coordinates, columns=['X', 'Y'])

# 각 점 사이의 거리 계산
df['Distance'] = np.sqrt(np.diff(df['X'], prepend=df['X'][0])**2 + np.diff(df['Y'], prepend=df['Y'][0])**2)

# 총 이동 거리 계산
total_distance = df['Distance'].sum()

# 미터당 계산 횟수 계산
computations_per_meter = len(df) / total_distance
print(total_distance)
print(len(df))

# 결과 출력
print(f"미터당 계산 횟수: {computations_per_meter:.2f}")


