# import os
# import tensorflow as tf 
# from tensorflow.python.client import device_lib

# os.environ["CUDA_VISIBLE_DEVICES"] = "0"


import tensorflow as tf
print("Is TensorFlow using GPU? ", tf.test.is_gpu_available())
tf.config.optimizer.set_jit(True)
# import tensorflow as tf
# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())

# import tensorflow as tf

print("TensorFlow Version:", tf.__version__)

# GPU 사용 가능 여부 확인
gpu_available = tf.config.list_physical_devices('GPU')
if gpu_available:
    print("GPU is available:", gpu_available)
    for gpu in gpu_available:
        details = tf.config.experimental.get_device_details(gpu)
        print("GPU Details:", details)
else:
    print("No GPU available. Running on CPU.")