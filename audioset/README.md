Installation Instructions for VGGish Pipeline

1) (Optional) Create either a Python or Conda virtualenv  
2) Clone this repo  
3) pip install the following packages, which are used by the VGGish model:  
pandas  
numpy  
scipy  
tensorflow  
resampy  
six  

4) pip install the following packages, which are used by the Youtube audio extractor:  

  pip install youtube_dl pafy ffmpy soundfile

5) Download the following two data files into the same directory as your VGGish python files:

* [VGGish model checkpoint](https://storage.googleapis.com/audioset/vggish_model.ckpt),
  in TensorFlow checkpoint format.
* [Embedding PCA parameters](https://storage.googleapis.com/audioset/vggish_pca_params.npz),
  in NumPy compressed archive format.

You can download them using the following two commands:  
$ curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt  
$ curl -O https://storage.googleapis.com/audioset/vggish_pca_params.npz  

6) Test the download
$ python vggish_smoke_test.py
If we see "Looks Good To Me", then we're all set.

OUTSTANDING ISSUES  

1) I can't figure out how to correctly clip audio that we download from Youtube. There are start_time and end_time parameters built into the youtube_dl library, but they don't seem to be implemented yet  
2) The wav file saves in hexadecimal format, which scipy doesn't know how to read (https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html). Hexadecimal should convert to a 16-bit PCM (int16), but I don't know how to do this in a way that retains .wav information, since scipy wants numbers in the range of [32768,32767] rather than [0,65535].

The following is in the .gitignore file:  
A Python Virtualenv with the necessary libraries installed  
The model checkpoint and the PCA parameters determined by Google's research  
.pyc files    
