OUTSTANDING ISSUES  

1) I can't figure out how to correctly clip audio that we download from Youtube. There are start_time and end_time parameters built into the youtube_dl library, but they don't seem to be implemented yet  
2) The wav file saves in hexadecimal format, which scipy doesn't know how to read (https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html). Hexadecimal should convert to a 16-bit PCM (int16), but I don't know how to do this in a way that retains .wav information, since scipy wants numbers in the range of [32768,32767] rather than [0,65535].
