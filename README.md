# HDV-Neurolex VGGish Pipeline

The following is in the .gitignore file:
A Python Virtualenv with the necessary libraries installed
The model checkpoint and the PCA parameters determined by Google's research
.pyc files  

Packages in the Virtualenv:  
youtube-dl: to extract audio from youtube videos  
pandas  
numpy  
scipy  
tensorflow  
resampy  
six  

All can be installed via "pip install ..."  

Python Files that the HDV team has written:  
pipeline.py #Modification of vggish_inference_demo.py. This takes all .wav files in the "audio_input" directory and creates JSON output files in the "json_output" directory 


audio_download.py #Reads Youtube video information from the "files_to_download.csv" file, strips the audio from each video, and saves the audio as a .wav file to the "audio_inputs" directory  

OUTSTANDING ISSUES  
1) I can't figure out how to correctly clip audio that we download from Youtube. There are start_time and end_time parameters built into the youtube_dl library, but they don't seem to be implemented yet  
2) The wav file saves in hexadecimal format, which scipy doesn't know how to read (https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html). Hexadecimal should convert to a 16-bit PCM (int16), but I don't know how to do this in a way that retains .wav information, since scipy wants numbers in the range of [32768,32767] rather than [0,65535].  


