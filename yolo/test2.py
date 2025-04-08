from ultralytics import YOLO
import os

# Load a pretrained YOLO model (recommended for training)
model = YOLO("runs/detect/train/weights/best.pt")


for i in os.listdir("test_data"):
    results = model.predict(source=f"test_data/{i}")  # Can also use video, directory, URL, etc.
    results[0].show(save=True, filename=f"result/{i}")  # Show the first image results("datasets/data/test/images/test80_jpg.rf.716acf9701dedfa40a35fab9a7aba8b7.jpg")
    input()
# Export the model to ONNX format