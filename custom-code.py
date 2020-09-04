import tensorflow as tf
import random
import numpy as np
import tempfile
import os, json
import tensorflow_datasets as tfds
import argparse
import sys
import time

time.sleep(60)

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(tf.distribute.experimental.CollectiveCommunication.NCCL)

with strategy.scope():
    config = tf.estimator.RunConfig(train_distribute=strategy, eval_distribute=strategy)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Initial learning rate')
    FLAGS, unparsed = parser.parse_known_args()
    print('FLAGS:')
    print(FLAGS)
    
    with open('/eos/user/d/dgolubov/katib-test.txt', 'w') as file:
        file.write('Hello World')
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(2048, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(1024),
        tf.keras.layers.Dense(512),
        tf.keras.layers.Dense(256),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(3)
    ])
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer=tf.keras.optimizers.Adam(FLAGS.learning_rate))
    #model.summary()

    def input_fn():
        split = tfds.Split.TRAIN
        dataset = tfds.load('iris', split=split, as_supervised=True)
        dataset = dataset.map(lambda features, labels: ({'dense_input':features}, labels))
        dataset = dataset.batch(32).repeat()
        return dataset

    os.system('mkdir /tmp/model_outputs')
    model_dir = '/tmp/model_outputs'
    keras_estimator = tf.keras.estimator.model_to_estimator(keras_model=model, model_dir=model_dir)

    print('Training...')
    train_result = keras_estimator.train(input_fn=input_fn, steps=100)
    print('Train result: {}'.format(train_result))
    print('Evaluating...')
    eval_result = keras_estimator.evaluate(input_fn=input_fn, steps=100)
    print('Eval result: {}'.format(eval_result))
