
// MIT License

// Copyright (c) 2022 luiree - Louis Reese

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.


#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstdio>
#include <sys/stat.h>
#include <math.h>
#include <deque>
#include <gsl/gsl_rng.h>

#include "bottleneck_ttrack7.h"

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

	sprintf (OFile, "trjINFO_den%f_TIP1_0.conf",First.dens);
	file_obj.open(OFile, ios::app);
	file_obj.write((char*)&First, sizeof(First)); 
	file_obj.close();
	delete OFile;
	
	return 0;
}

