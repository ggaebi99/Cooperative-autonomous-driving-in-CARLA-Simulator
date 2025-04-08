from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo12n.pt")

# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data="data.yaml", epochs=100)

# Evaluate the model's performance on the validation set
results = model.val()

# Perform object detection on an image using the model
results = model.predict(source="datasets/data/test/images/test80_jpg.rf.716acf9701dedfa40a35fab9a7aba8b7.jpg")  # Can also use video, directory, URL, etc.

# Display the results
results[0].show()  # Show the first image results("datasets/data/test/images/test80_jpg.rf.716acf9701dedfa40a35fab9a7aba8b7.jpg")

# Export the model to ONNX format