"""Regression check: BDE checkpoint reload must preserve Adam slots and next update."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
os.environ['TF_NUM_INTRAOP_THREADS']='1'
os.environ['TF_NUM_INTEROP_THREADS']='1'
import tempfile
from pathlib import Path
import numpy as np
import tensorflow as tf

tf.keras.utils.set_random_seed(31)
model=tf.keras.Sequential([tf.keras.layers.Dense(3,input_shape=(2,)),tf.keras.layers.Dense(1)])
model.compile(optimizer='adam',loss='mse')
x=np.arange(32,dtype='float32').reshape(16,2)/32
y=np.sin(x[:,0])
model.train_on_batch(x,y)
model.train_on_batch(x,y)
with tempfile.TemporaryDirectory() as directory:
    path=Path(directory)/'checkpoint.keras'
    model.save(path)
    restored=tf.keras.models.load_model(path)
    assert int(restored.optimizer.iterations)==int(model.optimizer.iterations)==2
    for a,b in zip(model.optimizer.variables(),restored.optimizer.variables()):
        np.testing.assert_array_equal(a.numpy(),b.numpy())
    model.train_on_batch(x,y);restored.train_on_batch(x,y)
    for a,b in zip(model.weights,restored.weights):
        np.testing.assert_array_equal(a.numpy(),b.numpy())
print('PASS: optimizer slots, iteration and next training update are preserved')
