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

5) pip install the following packages, which are used by the Youtube audio extractor:  

#Please List Necessary Packages  

4) Download the following two data files into the same directory as your VGGish python files:

* [VGGish model checkpoint](https://storage.googleapis.com/audioset/vggish_model.ckpt),
  in TensorFlow checkpoint format.
* [Embedding PCA parameters](https://storage.googleapis.com/audioset/vggish_pca_params.npz),
  in NumPy compressed archive format.

You can download them using the following two commands:  
$ curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt  
$ curl -O https://storage.googleapis.com/audioset/vggish_pca_params.npz  

5) Test the download
$ python vggish_smoke_test.py
If we see "Looks Good To Me", then we're all set.

