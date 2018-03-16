# Copyright 2017 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

r"""

Pipeline that reads in all wav files in a folder and then outputs them as json objects 

Usage:
  $ python vggish_inference_demo.py --wav_file_direc /path/to/wave/file/directory \
                                    --embedding_direc /path/to/embeddings/directory
                                    --checkpoint /path/to/model/checkpoint \
                                    --pca_params /path/to/pca/params

"""

from __future__ import print_function

import numpy as np
from scipy.io import wavfile
import six
import tensorflow as tf

from os import listdir
from os.path import join
import json

import vggish_input
import vggish_params
import vggish_postprocess
import vggish_slim

flags = tf.app.flags

flags.DEFINE_string(
    'wav_file_direc', None,
    'Path to a directory of wav files. Should contain signed 16-bit PCM samples. ')

flags.DEFINE_string(
    'checkpoint', 'vggish_model.ckpt',
    'Path to the VGGish checkpoint file.')

flags.DEFINE_string(
    'pca_params', 'vggish_pca_params.npz',
    'Path to the VGGish PCA parameters file.')

flags.DEFINE_string(
    'embedding_direc', None,
    'Path to the directory in which output embeddings will be stored in JSON format.')

FLAGS = flags.FLAGS


def main(_):
  # In this simple example, we run the examples from a single audio file through
  # the model. If none is provided, we generate a synthetic input.

  #Read in .wav files from input directory, create array of wav_file names

  wav_files = listdir(FLAGS.wav_file_direc)
  
  #Initialize array of batches and read each wav_file in wav_files array
  batches = []

  for wav_file in wav_files:
    examples_batch = vggish_input.wavfile_to_examples(join(FLAGS.wav_file_direc,wav_file))
    batches.append(examples_batch)

  # Prepare a postprocessor to munge the model embeddings.
  pproc = vggish_postprocess.Postprocessor(FLAGS.pca_params)

  output_dicts = []
  with tf.Graph().as_default(), tf.Session() as sess:
    # Define the model in inference mode, load the checkpoint, and
    # locate input and output tensors.
    vggish_slim.define_vggish_slim(training=False)
    vggish_slim.load_vggish_slim_checkpoint(sess, FLAGS.checkpoint)
    features_tensor = sess.graph.get_tensor_by_name(
        vggish_params.INPUT_TENSOR_NAME)
    embedding_tensor = sess.graph.get_tensor_by_name(
        vggish_params.OUTPUT_TENSOR_NAME)


    #Create a JSON output file for each audio file
    for batch in batches:
      # Run inference and postprocessing.
      [embedding_batch] = sess.run([embedding_tensor],
                                   feed_dict={features_tensor: batch})
      postprocessed_batch = pproc.postprocess(embedding_batch)

      #Create a dictionary of embeddings to be dumped into a json file
      output_dict = {}
      count = 0
      for embedding in postprocessed_batch:
        output_dict["t"+str(count)] = embedding
        count+=1

      output_dicts.append(output_dict)

  for i in range(0, len(wav_files)):
    with open(join(FLAGS.embedding_direc,wav_files[i][:-3])+"json", 'w') as outfile:
      json.dump(output_dicts[i], outfile)



if __name__ == '__main__':
  tf.app.run()
