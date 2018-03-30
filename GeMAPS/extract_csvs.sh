for f in $(ls -1 inputs/*.wav);
do for conf in $(ls -1 openSMILE-2.1.0/config/*.conf);
do openSMILE-2.1.0/inst/bin/SMILExtract -C $conf -I $f -O outputs/f.conf.csv $f.mfcc.htk ; 
done;
done;