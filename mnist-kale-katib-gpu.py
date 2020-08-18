#!/usr/bin/env python
# coding: utf-8

# In[26]:

# A comment
import tensorflow as tf
print(tf.__version__)
import numpy as np
import os
import time


# In[2]:


nodes_number = 32
learning_rate = 0.0001


# # MNIST classification

# In[3]:


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0


# In[4]:


def filter_36(x, y):
    keep = (y == 3) | (y == 6)
    x, y = x[keep], y[keep]
    y = y == 3
    return x,y

print("Number of unfiltered training examples:", len(x_train))
print("Number of unfiltered test examples:", len(x_test))

x_train, y_train = filter_36(x_train, y_train)
x_test, y_test = filter_36(x_test, y_test)

print("Number of filtered training examples:", len(x_train))
print("Number of filtered test examples:", len(x_test))


# In[18]:
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

with strategy.scope():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, [3, 3], activation='relu', input_shape=(28,28,1)))
    model.add(tf.keras.layers.Conv2D(64, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.Flatten())

    model.add(tf.keras.layers.Dense(nodes_number, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(1))

model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate), metrics=['accuracy'])
model.summary()


# In[19]:


print(x_train.shape)


# In[33]:


start = time.time()
with strategy.scope():
    model.fit(x_train, y_train, batch_size=128, epochs=200, verbose=1, validation_data=(x_test, y_test))
end = time.time()
print('Training took', end - start, 'seconds')
print('img/sec =', x_train.shape[0] / (end - start))


# In[34]:


test_acc = model.evaluate(x_test, y_test)[1]


# In[35]:


print(test_acc)


# In[ ]:




