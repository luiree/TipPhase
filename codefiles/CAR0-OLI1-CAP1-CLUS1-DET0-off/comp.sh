#!/bin/bash

EXPECTED_ARGS=6
ARGC=$#

if [ $ARGC -eq $EXPECTED_ARGS ]; then
	CAR=$1	#cargo monomers
	OLI=$2 #cargo oligomers CAR/OLI mutually exclusive
	CAP=$3 #gtp cap independent of other settings
	CLUS=$4 #clustering works for both CAR/OLI setting
	DET=$5 #motor detachment from clusters yes/no
	OFF=$6 #factor detachment from clusters

	HOMEX=/home/louis
	cwd=`pwd`

	PREmain="main_ttrack7_$CAR$OLI$CAP$CLUS$DET"
	PREclass="bottleneck_ttrack7_$CAR$OLI$CAP$CLUS$DET"

	CARGO="tt7_CAR$CAR-OLI$OLI-CAP$CAP-CLUS$CLUS-DET$DET-OFF$OFF.out"
	NewDir="CAR$CAR-OLI$OLI-CAP$CAP-CLUS$CLUS-DET$DET-OFF$OFF"

	g++ -I/usr/include -I$HOMEX/lib/gsl/include -O3 -c  $PREmain.cpp
	g++ -I/usr/include -I$HOMEX/lib/gsl/include -O3 -c  $PREclass.cpp
	g++ -o $CARGO $PREclass.o $PREmain.o -L$HOMEX/lib/gsl/lib/ -static -O3 -lgsl -lgslcblas -lm 

else
        printf  "\nInvalid number of arguments, please check the inputs and try again\n"
		printf  "
		CAR=#1	OLI=#2 CAP=#3 CLUS= #4 DET=#5 \n 
		#cargo monomers \n
		#cargo oligomers and monomers are mutually exclusive \n
		#gtp cap is independent other settings \n
		#clustering is possible for both CAR/OLI setting \n
		#motor detachment from clusters yes/no 1/0 \n
		#motor detachment from clusters factor reduction \n" 

fi;


