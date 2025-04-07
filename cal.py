import numpy as np
import json

def calculate_metrics(data):
    total_distance = {}
    mode_times = {}
    
    for i in range(len(data) - 1):
        x1, y1, mode1, time1 = data[i]
        x2, y2, mode2, time2 = data[i + 1]
        
        # 유클리드 거리 계산
        distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # 모드별 이동 거리와 계산 시간 누적
        if mode1 not in total_distance:
            total_distance[mode1] = 0
            mode_times[mode1] = 0
        total_distance[mode1] += distance
        mode_times[mode1] += time1
    
    # 마지막 데이터 포인트의 계산 시간 추가
    last_mode, last_time = data[-1][2], data[-1][3]
    if last_mode not in mode_times:
        mode_times[last_mode] = 0
    mode_times[last_mode] += last_time
    
    # 모드별 1미터당 평균 계산 시간 계산
    mode_time_per_meter = {mode: (mode_times[mode] / total_distance[mode]) if total_distance[mode] > 0 else 0 
                           for mode in mode_times}
    
    return total_distance, mode_times, mode_time_per_meter

def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='UTF8') as file:
        data = [
            (float(line.split(',')[0]), float(line.split(',')[1]), 
             line.split(',')[2] == 'True', float(line.split(',')[3]))
            for line in file.readlines()
        ]
    return data

def write_results_to_file(file_path, total_distance, mode_times, mode_time_per_meter):
    results = {
        "모드별 총 거리": total_distance,
        "모드별 총 계산시간": mode_times,
        "모드별 1미터당 평균 계산 시간": mode_time_per_meter
    }
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

# 파일 입력 및 결과 저장
input_file = 'cal.txt'  # 입력 파일 경로
output_file = 'output_results.json'  # 결과 저장 파일 경로

data = read_data_from_file(input_file)
total_distance, mode_times, mode_time_per_meter = calculate_metrics(data)
write_results_to_file(output_file, total_distance, mode_times, mode_time_per_meter)
