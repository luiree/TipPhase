/*
 *  main_ttrack7.cpp
 *  
 *  Created by Louis Reese on 24.08.10.
 *  Copyright 2020 Louis Reese. All rights reserved.
 *	
 *	Adapted for cargo clustering study.
 *	Time dependent phenomna.
 *
 */

#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstdio>
#include <sys/stat.h>
#include <math.h>
#include <deque>
#include <gsl/gsl_rng.h>

#include "bottleneck_ttrack7.h"

// The def statement is completed during compilation 0/1

using namespace std;

int main(int argc, char *argv[])
{	
	RING First;
	First.InitClass(argv);
	First.RngInit(argv);
	
	First.EquiLanes(argv);
	while(First.KIN(argv)>0){};
	First.InitLanesNoShock(argv);

	for(int runs=0; runs<1; runs++){
		while(First.KIN(argv)>0){}; 
	}

	// Opening file a configuration to save the class First,
	ofstream file_obj; 
	char * OFile;
	OFile = new char[80];
	// Choosing cargo clustering also means to choose cargo
	// Careful not all combinations of cases are valid choices

	sprintf (OFile, "trjINFO_den%f_TIP1_OLIGO.conf",First.dens);
	file_obj.open(OFile, ios::app);
	file_obj.write((char*)&First, sizeof(First)); 
	file_obj.close();
	delete OFile;
	
	return 0;
}

