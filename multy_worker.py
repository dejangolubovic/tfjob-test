import tensorflow_datasets as tfds
import tensorflow as tf
import argparse
import sys
import os
import json

tfds.disable_progress_bar()

FLAGS = None
loss = 100

def train_evalaute():
  BUFFER_SIZE = 10000
  BATCH_SIZE = 64

  def input_fn(mode, input_context=None):
    datasets, info = tfds.load(name='mnist',
                                  with_info=True,
                                  as_supervised=True)
    mnist_dataset = (datasets['train'] if mode == tf.estimator.ModeKeys.TRAIN else
                     datasets['test'])

    def scale(image, label):
      image = tf.cast(image, tf.float32)
      image /= 255
      return image, label

    if input_context:
      mnist_dataset = mnist_dataset.shard(input_context.num_input_pipelines,
                                          input_context.input_pipeline_id)
    return mnist_dataset.map(scale).cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

  def model_fn(features, labels, mode):
    if os.environ.get('TF_CONFIG') is not None:
        print('TF_CONFIG:', os.environ['TF_CONFIG'])
        TFCONF_dict = json.loads(os.environ['TF_CONFIG'])
        print('task:', TFCONF_dict['task'])
    else:
        print("No TFCONFIG")

    print('mode =', mode)

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    logits = model(features, training=False)

    if mode == tf.estimator.ModeKeys.PREDICT:
      print('Predicting')
      predictions = {'logits': logits}
      return tf.estimator.EstimatorSpec(labels=labels, predictions=predictions)

    optimizer = tf.compat.v1.train.GradientDescentOptimizer(
        learning_rate=FLAGS.learning_rate)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction=tf.keras.losses.Reduction.NONE)(labels, logits)
    loss = tf.reduce_sum(loss) * (1. / BATCH_SIZE)
    if mode == tf.estimator.ModeKeys.EVAL:
      print('Evaluating')
      return tf.estimator.EstimatorSpec(mode, loss=loss)

    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        train_op=optimizer.minimize(
            loss, tf.compat.v1.train.get_or_create_global_step()))

  strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(tf.distribute.experimental.CollectiveCommunication.NCCL)
  config = tf.estimator.RunConfig(train_distribute=strategy, eval_distribute=strategy)

  classifier = tf.estimator.Estimator(
      model_fn=model_fn, model_dir='/tmp/multiworker', config=config)

  print('Starting the Job')
  metrics = tf.estimator.train_and_evaluate(
      classifier,
      train_spec=tf.estimator.TrainSpec(input_fn=input_fn),
      eval_spec=tf.estimator.EvalSpec(input_fn=input_fn)
  )
  loss = metrics[0]['loss']
  print('Job Completed')
  print('metrics')
  print(metrics)
  print('loss')
  print(loss)
  print(os.listdir('/tmp/multiworker'))

def main(_):
  train_evalaute()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--learning_rate', type=float, default=0.001, help='Initial learning rate')
  
  FLAGS, unparsed = parser.parse_known_args()
  tf.compat.v1.app.run(main=main, argv=[sys.argv[0]] + unparsed)
