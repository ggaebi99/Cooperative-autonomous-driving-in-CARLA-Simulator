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