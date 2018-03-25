Installation Instructions

First, we need to ensure that the build system is up to speed. The easiest way to do this is with Homebrew. Once you install Homebrew, do the following commands:  

brew install autoconf automake libtool
brew upgrade gawk

Then, download the stable release of openSMILE from the audEERING website (openSMILE 2.1):  
https://audeering.com/technology/opensmile/  

Then, use the following commands to compile openSmile (see section 2.2 here for more details):
https://www.audeering.com/research-and-open-source/files/openSMILE-book-latest.pdf

tar -zxvf openSMILE-2.x.x.tar.gz
cd openSMILE-2.x.x
sh buildStandalone.sh  

To then ensure that openSMILE was installed correctly, try the following command:

inst/bin/SMILExtract -h


TODO: Concatenate the default feature extractors in the /config directory of openSMILE

What is in the .gitignore:

My installation directory of openSMILE

