import tensorflow as tf
import random
import numpy as np
import tensorflow_datasets as tfds
import tempfile
import os, json

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(tf.distribute.experimental.CollectiveCommunication.NCCL)
config = tf.estimator.RunConfig(train_distribute=strategy, eval_distribute=strategy)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3)
])
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer='adam')
#model.summary()

def input_fn():
    split = tfds.Split.TRAIN
    dataset = tfds.load('iris', split=split, as_supervised=True)
    dataset = dataset.map(lambda features, labels: ({'dense_input':features}, labels))
    dataset = dataset.batch(32).repeat()
    return dataset

model_dir = tempfile.mkdtemp()
keras_estimator = tf.keras.estimator.model_to_estimator(keras_model=model, model_dir=model_dir)
print('Training...')
keras_estimator.train(input_fn=input_fn, steps=100000)
print('Evaluating...')
eval_result = keras_estimator.evaluate(input_fn=input_fn, steps=100)
print('Eval result: {}'.format(eval_result))
