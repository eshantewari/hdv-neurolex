import youtube_dl
import pandas as pd
import os
import traceback

CSV = "files_to_download.csv"

# create directory
savedir = "./audio_input/"
if not os.path.exists(savedir):
    os.makedirs(savedir)

def make_savepath(title, savedir=savedir):
    return os.path.join(savedir, "%s.wav" % title)


# create YouTube downloader
options = {
    'format': 'bestaudio/best', # choice of quality
    'extract-audio' : True,      # only keep the audio
    'audio-format' : "wav",      # convert to wav 
    'no-playlist' : True,        # only download single song, not playlist
    'outtmpl': '%(id)s',
}        
ydl = youtube_dl.YoutubeDL(options)


with ydl:

    # read in videos CSV with pandas
    df = pd.read_csv(CSV)
    df.Link = df.Link.map(str.strip)  # strip space from URLs

    # for each row, download
    for _, row in df.iterrows():
        print "Downloading: %s from %s..." % (row.Title, row.Link)
        
        # download location, check for progress
        savepath = make_savepath(row.Title)
        try:
            os.stat(savepath)
            print "%s already downloaded, continuing..." % savepath
            continue

        except OSError:
            # download video
            try:
                result = ydl.extract_info(row.Link, download=True)
                os.rename(result['id'], savepath)
                print "Downloaded and converted %s successfully!" % savepath

            except Exception as e:
                print "Can't download audio! %s\n" % traceback.format_exc()