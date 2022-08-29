// MIT License
//
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
#include <fstream>
#include <deque>
#include <cstdio>
#include <cstdlib>

using namespace std;


int main(int argc, char *argv[])
{
	int Size = atoi(argv[2]);
	int Spec = atoi(argv[3]);

	deque<double> DENSITY1(Size, 0);
	deque<double> DENSITY2(Size, 0);
	int occ, vac, jump, count=0, x=0;
	FILE *TFile=fopen(argv[1],"r");

	while (!feof(TFile)){
		for (int i=0; i<Size; i++) 
		{
		//	char trans=block[i];
			fscanf(TFile,"%d",&occ);
			if (occ>0 && Spec == 1)
				DENSITY1.at(i) += occ/1.0;
			if (occ>1 && Spec == 2)
				DENSITY2.at(i) += occ/2.0;


		}
		count++;
	}
	
	if (Spec == 1){
		for (int i=0; i<DENSITY1.size(); i++) 
		{
			cout << (double)i << " " << DENSITY1.at(i)/(double)count << endl;
		}
	}
	else if (Spec == 2){
		for (int i=0; i<DENSITY2.size(); i++) 
		{
			cout << (double)i << " " << DENSITY2.at(i)/(double)count << endl;
		}
	}

	fclose(TFile);

	return 0;
}

