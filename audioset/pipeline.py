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
  $ python vggish_inference_demo.py 

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



def main(_):
  # In this simple example, we run the examples from a single audio file through
  # the model. If none is provided, we generate a synthetic input.

  #Read in .wav files from input directory, create array of wav_file names

  wav_file_direc = "./audio_input/"
  embedding_direc = "./json_output/"
  checkpoint = "vggish_model.ckpt"
  pca_params = "vggish_pca_params.npz"


  wav_files = listdir(wav_file_direc)
  
  #Initialize array of batches and read each wav_file in wav_files array
  batches = []

  for wav_file in wav_files:
    if "wav" in wav_file:
      print(join(wav_file_direc,wav_file))
      examples_batch = vggish_input.wavfile_to_examples(join(wav_file_direc,wav_file))
      batches.append(examples_batch)

  # Prepare a postprocessor to munge the model embeddings.
  pproc = vggish_postprocess.Postprocessor(pca_params)

  output_dicts = []
  with tf.Graph().as_default(), tf.Session() as sess:
    # Define the model in inference mode, load the checkpoint, and
    # locate input and output tensors.
    vggish_slim.define_vggish_slim(training=False)
    vggish_slim.load_vggish_slim_checkpoint(sess, checkpoint)
    features_tensor = sess.graph.get_tensor_by_name(
        vggish_params.INPUT_TENSOR_NAME)
    embedding_tensor = sess.graph.get_tensor_by_name(
        vggish_params.OUTPUT_TENSOR_NAME)


    output_sequences = []
    #Create a JSON output file for each audio file
    for batch in batches:
      # Run inference and postprocessing.
      [embedding_batch] = sess.run([embedding_tensor],
                                   feed_dict={features_tensor: batch})
      postprocessed_batch = pproc.postprocess(embedding_batch)

      seq_example = tf.train.SequenceExample(
          feature_lists=tf.train.FeatureLists(
              feature_list={
                  vggish_params.AUDIO_EMBEDDING_FEATURE_NAME:
                      tf.train.FeatureList(
                          feature=[
                              tf.train.Feature(
                                  bytes_list=tf.train.BytesList(
                                      value=[embedding]))
                              for embedding in postprocessed_batch
                          ]
                      )
              }
          )
      )

      output_sequences.append(seq_example)

  for i in range(0, len(wav_files)):
    with open(join(embedding_direc,wav_files[i][:-3])+"json", 'w') as outfile:
      json.dump(output_sequences[i], outfile)



if __name__ == '__main__':
  tf.app.run()
