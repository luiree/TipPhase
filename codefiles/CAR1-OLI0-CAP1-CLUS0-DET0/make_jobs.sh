#/bin/bash

runfile=$1
rng=67
rm run.sh

for i in 20 40 60 80 100 120 140 160 180; 
do 
	cp job.pbs job$i.pbs
	echo "./"$runfile $i $rng >> job$i.pbs
	echo "qsub job$i.pbs"  >> run.sh

done

chmod +x run.sh 
./run.sh
