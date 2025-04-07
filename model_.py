import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, LSTM, GRU
import matplotlib.pyplot as plt

# 
def load_txt_data(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            values = list(map(float, line.strip().split(",")))  # 쉼표 기준으로 분리 후 float 변환
            data.append(values)
    
    return np.array(data)

# 
filename = "M2501/D0125/yaw_data.txt"  # 사용할 TXT 파일 이름
data = load_txt_data(filename)

X = data[:, :-1]  # 마지막 열을 제외한 5개의 feature
y = data[:, -1]   # 마지막 열이 label

# 4️⃣ RNN 입력 형식으로 변환 (batch_size, time_steps, features)
time_steps = X.shape[1]  # Feature 개수를 Time Step으로 사용
features = 1             # 단일 feature씩 입력

X_reshaped = X.reshape((X.shape[0], time_steps, features))
y_reshaped = y.reshape((-1, 1))  # Label도 (batch_size, 1) 형태

# 5️⃣ Train, Validation, Test 데이터 나누기
X_train, X_temp, y_train, y_temp = train_test_split(X_reshaped, y_reshaped, test_size=0.2, random_state=42)  # 80% Train, 20% Temp
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)  # 10% Validation, 10% Test

# 데이터 형태 출력
print("X_train Shape:", X_train.shape)  # (Train 샘플 개수, Time Steps, Features)
print("X_val Shape:", X_val.shape)      # (Validation 샘플 개수, Time Steps, Features)
print("X_test Shape:", X_test.shape)    # (Test 샘플 개수, Time Steps, Features)

# 6️⃣ LSTM 모델 생성
model_1 = Sequential([
    SimpleRNN(10, activation='tanh', input_shape=(time_steps, features)),  # SimpleRNN Layer
    Dense(1, activation='sigmoid')  # 이진 분류용 출력층
])

# 7️⃣ 모델 컴파일
model_1.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_1.summary()

# 8️⃣ 모델 학습 (Validation Set 포함)
history_1 = model_1.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))

# 9️⃣ 모델 평가 (Test Set)
test_loss_1, test_acc_1 = model_1.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc_1:.4f}")

# 🔟 예측 실행
predictions_1 = model_1.predict(X_test)
print("Predictions:", predictions_1.flatten())

model_2 = Sequential([
    LSTM(10, activation='tanh', input_shape=(time_steps, features)),  # SimpleRNN Layer
    Dense(1, activation='sigmoid')  # 이진 분류용 출력층
])

# 7️⃣ 모델 컴파일
model_2.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_2.summary()

# 8️⃣ 모델 학습 (Validation Set 포함)
history_2 = model_2.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))

# 9️⃣ 모델 평가 (Test Set)
test_loss_2, test_acc_2 = model_2.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc_2:.4f}")

# 🔟 예측 실행
predictions_2 = model_2.predict(X_test)
print("Predictions:", predictions_2.flatten())

model_3 = Sequential([
    GRU(10, activation='tanh', input_shape=(time_steps, features)),  # SimpleRNN Layer
    Dense(1, activation='sigmoid')  # 이진 분류용 출력층
])

# 7️⃣ 모델 컴파일
model_3.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_3.summary()

# 8️⃣ 모델 학습 (Validation Set 포함)
history_3 = model_3.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))

# 9️⃣ 모델 평가 (Test Set)
test_loss_3, test_acc_3 = model_3.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc_2:.4f}")

# 🔟 예측 실행
predictions_3 = model_3.predict(X_test)
print("Predictions:", predictions_3.flatten())


def plot_training_history(history):
    plt.figure(figsize=(12, 4))

    # Loss 그래프
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Over Epochs')
    plt.legend()

    # Accuracy 그래프
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Over Epochs')
    plt.legend()

    plt.show()

# 학습 그래프 호출
def plot_comparison(history_1, history_2, history_3):
    plt.figure(figsize=(12, 6))

    # Loss 비교
    plt.subplot(1, 2, 1)
    plt.plot(history_1.history['loss'], label='SimpleRNN - Train Loss')
    plt.plot(history_1.history['val_loss'], label='SimpleRNN - Val Loss')

    plt.plot(history_2.history['loss'], label='LSTM - Train Loss')
    plt.plot(history_2.history['val_loss'], label='LSTM - Val Loss')

    plt.plot(history_3.history['loss'], label='GRU - Train Loss')
    plt.plot(history_3.history['val_loss'], label='GRU - Val Loss')

    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Comparison')
    plt.legend()

    # Accuracy 비교
    plt.subplot(1, 2, 2)
    plt.plot(history_1.history['accuracy'], label='SimpleRNN - Train Acc')
    plt.plot(history_1.history['val_accuracy'], label='SimpleRNN - Val Acc')

    plt.plot(history_2.history['accuracy'], label='LSTM - Train Acc')
    plt.plot(history_2.history['val_accuracy'], label='LSTM - Val Acc')

    plt.plot(history_3.history['accuracy'], label='GRU - Train Acc')
    plt.plot(history_3.history['val_accuracy'], label='GRU - Val Acc')

    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Comparison')
    plt.legend()

    plt.show()

# 모델 비교 그래프 출력
plot_comparison(history_1, history_2, history_3)