import re

# 파일 읽기
with open('second.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

cleaned_coordinates = []

# 이상한 단어들
invalid_words = ['보정값', 'True']

# 각 줄 처리
for line in lines:
    # 이상한 단어 제거
    for word in invalid_words:
        line = line.replace(word, '')
    
    # 좌표 추출
    matches = re.findall(r'(-?\d+\.\d+)', line)
    
    # X, Y 쌍으로 묶기
    if len(matches) >= 2:
        for i in range(0, len(matches)-1, 2):
            x, y = float(matches[i]), float(matches[i+1])
            cleaned_coordinates.append((x, y))

# 결과 출력
for coord in cleaned_coordinates:
    print(f"X: {coord[0]}, Y: {coord[1]}")

# 결과를 새 파일에 저장
with open('cleaned_coordinates.txt', 'w', encoding='utf-8') as outfile:
    for coord in cleaned_coordinates:
        outfile.write(f"X: {coord[0]}, Y: {coord[1]}\n")