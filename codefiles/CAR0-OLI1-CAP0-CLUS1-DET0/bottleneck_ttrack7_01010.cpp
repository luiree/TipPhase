
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
#include <deque>
#include <algorithm>
#include <iterator>
#include <math.h>

#include "bottleneck_ttrack7.h"

// The def statement is completed during compilation 0/1
#define CARGO 0 
#define OLIGO 1
#define CLUS 1 
#define CAP 0 
#define DET 0
// motor detachment from CLUS 1 DETACH 1

using namespace std;

// Initialise GSL random number generator
// parameter[2] specifies a seed value from the command line (2nd argument)
void RING::RngInit(char *parameters[]){
       r = gsl_rng_alloc(gsl_rng_mt19937);
       RanInit=(long int)atoi(parameters[2]);
       gsl_rng_set(r, RanInit);
}

//Initiallise constants and simulation parmeters as well as lattices
void RING::InitClass(char *parameters[]){
	Size=1000;	// Size of the lattice in the simulation (one site is 8.4 nm)
	CONC=atoi(parameters[1]);	// Motor concentration in [nM] (1st commandline argumen)
	speed1=20;	// (19.8)Motor speed on GDP microtubule lattice 10 uM/min (single molecule)
			// This sets the unit timescale (seconds)
	off=0.08;	// Motor detachment rate from GDP lattice in units of tau (inverse run-length)
			// run length around 2 uM (1.78 um). 211 sites. takes 12 (10.66) seconds.
	on=CONC * 0.00002;	// Motor on rate. Landing rate extracted from 1nM dataset
				// that had been analysed using Kymobutler
	K=on/off;	// Calculate motor association rate constant
	rho=K/(K+1);	// Calculate motor equilibrium occupation probability (density)
	dens=rho;	// Define density
	alpha=speed1*rho;	// Define motor entry rate at the beginning of the lattice

	grow=0.3*speed1;		// ----0.3; -- // MT growth sets the timescale 3 uM/min ---

	speed2=speed1; //0.50;	// Motor speed on GTPgS (tip) 5 uM/min
			// The motor hopping rate depends on the nucleotide state of the MT lattice 
			// However was not measure at the single molecule level
	//beta=0.5*speed2; //0.50;	// Motor detachment rate at the end of the lattice
	k1=0.0;		// ----0.14;//Maturation Surrey Missing ref
	hydr=0.0;		// ----0.024; Set's the size of the GTP cap to 40  

	off2=0.5*off;	// Motor detachment from cluster
	beta=speed2; //0.5*speed2; //0.50;	// Motor detachment rate at the end of the lattice
	//beta=0.5*speed2; //0.50;	// Motor detachment rate at the end of the lattice

	onCARG=0.0;
	offCARG=0.0;
	Kcarg=0;
	rhoCARG=0;

	onOLIGO=0.03;	// Cluster formation reactions
	offOLIGO=0.01;
	Koligo=onOLIGO/offOLIGO;
	rhoOLIGO=Koligo/(Koligo+1);

	MAX_count=10000;		// Set the amount of datapoints to be acquired
}

// Initialise 
void RING::EquiLanes(char *parameters[]){
	Time=0.0;	// Initialize simulation time
	FLAG=0;		// FLAG for equilibration of the density profile before measurements
	Clock=100*Size;	// Set equilibration time before measurement begins to 100xsystem size
	count=0;	// Set counter
	RING.clear();	// Initialise the lattice
	RING.resize(3, std::deque<unsigned int>(Size,0)); // Lattice definition
			// RING[0] Motor occupation (0/2)
			// RING[1] Nucleotide state of the lattice (hydrolysed:0; mature:1; GTP:2)
			// RING[2] TIP1 occupation (0/1)
}

void RING::InitLanes(char *parameters[]){
	FLAG=1;		// Set FLAG for measurement start
	Clock_count=(double)Size/speed1;	// Set the time interval between measurements
	count=0;			// Set counter
	Clock=Time;			// Set first measurement Time
	
	// Create a 'transfer event', i.e. the first 100 lattice sites are
	// occupied by motors and cargo, depending on simulation runs
	for(int i=0; i<100; i++){
		RING[0][i]=2;	// Fill with motors
	}
}

void RING::InitLanesNoShock(char *parameters[]){
	FLAG=1;		// Set FLAG for measurement start
	Clock_count=(double)Size/speed1;	// Set the time interval between measurements
	count=0;			// Set counter
	Clock=Time;			// Set first measurement Time
}

// Implementation of motors moving at speed1
void RING::makeDRIVE1(){
	// if(FLAG>0)
	// {for (int k=0; k<RING[1].size(); k++) std::cout << RING[0][k] ;
	// std::cout << "\n";
	// for (int k=0; k<RING[1].size(); k++) std::cout << RING[2][k] ;
	// std::cout << "\n";
	// }
	position=gsl_rng_uniform_int(r,DRIVE1.size());	// Randomly choose which of the allowed motors moves
	RING[0][DRIVE1[position]]=0;					// Update the position of the motor, remove at old place.
	RING[0][DRIVE1[position]+1]=2;					// Add motor to the new spot (+1).
	if (RING[2][DRIVE1[position]] > 0)
	{
		RING[2][DRIVE1[position]+1]= RING[2][DRIVE1[position]];
		RING[2][DRIVE1[position]]=0;
		/*
		If the chosen motor with cargo is part of a larger cluster, the entire cluster
		consisting of motors and cargos moves as a condensate in an parallel update move.
		All particles of the cluster move in sync.
		*/
		if (DRIVE1[position] > 0 )
		{
			int k=1;
			while (DRIVE1[position]-k > 0 && RING[0][DRIVE1[position]-k] > 0 && RING[2][DRIVE1[position]-k] > 0)
			{
				
				RING[0][DRIVE1[position]-k+1]= RING[0][DRIVE1[position]-k];
				RING[0][DRIVE1[position]-k]=0;
				RING[2][DRIVE1[position]-k+1]= RING[2][DRIVE1[position]-k];
				RING[2][DRIVE1[position]-k]=0;
				k++;
			}
		}
	}
}


// Attachment of motors
void RING::makeON(){
	position=gsl_rng_uniform_int(r,ON.size());	// Randomly choose a free site
	RING[0][ON[position]]=2;					// Position the motor
	RING[2][ON[position]]=1+gsl_rng_uniform_int(r,Koligo); // floor Koligo in order to have integer number.
}

// Detachment of motors
void RING::makeOFF(){
	position=gsl_rng_uniform_int(r,OFF.size());	// Randomly choose a motor
	RING[0][OFF[position]]=0;					// Remove the particle
	RING[2][OFF[position]]=0;					// Remove any eventual cargo which may be bound to the motor
}

// Detachment of motors FROM clusters
void RING::makeOFF2(){
	position=gsl_rng_uniform_int(r,OFF2.size());	// Randomly choose a motor
	RING[0][OFF2[position]]=0;					// Remove the particle
	RING[2][OFF2[position]]=0;					// Remove any eventual cargo which may be bound to the motor
}


// Detachment of motors at the microtubule tip. It is important to keep this seperate 
// in order to control the ensuing phase phenomena, i.e. traffic jam formation
void RING::makeTIPOFF(){
	RING[0][RING[0].size()-1]=0;
#if OLIGO || CARGO
	RING[2][RING[2].size()-1]=0;
#endif
}

// Growth events are implemented as push_back() and need to be carried out on all 3 lattices
void RING::makeGRO(){
	RING[0].push_back(0);
	RING[0].pop_front();
	RING[1].push_back(2);
	RING[1].pop_front();
	RING[2].push_back(0);
	RING[2].pop_front();
}

// Feeding rate onto the lattice at the lattice start. Important to avoid spatial profiles which
// would hamper a clear distinction between different phenomena of interest here.
void RING::makeIN(){
	RING[0][0]=2;
	RING[2][0]=1+gsl_rng_uniform_int(r,Koligo);
}

// Cluster growth/shrinkage by attachment and detachment of cargo
void RING::makeOLIGOon(){
	position=gsl_rng_uniform_int(r,ONoligo.size());
	RING[2][ONoligo[position]]=RING[2][ONoligo[position]]+1;
}
void RING::makeOLIGOoff(){
	position=gsl_rng_uniform_int(r,OFFoligo.size());
	RING[2][OFFoligo[position]]=RING[2][OFFoligo[position]]-1;
}

/*
The KIN function keeps track of all the possible moved in the system
as well as the Gillespie algorithm and writing to files (the time recording version only)
*/
int RING::KIN(char *parameters[]) //, std::fstream &tasep, std::fstream &out, std::fstream &cap)
{
	// Clean all the ncessary containers
	DRIVE1.clear();
	ON.clear();
	OFF.clear();
	OFF2.clear();
	ONoligo.clear();
	OFFoligo.clear();

	// Iterate through the entire lattice and determine possible moves
	// Reminder 
	// RING[0] motor lattice
	// RING[1] nucleotide lattice
	// RING[2] cargo lattice
		
    for (int k=0; k<RING[0].size()-1; k++) 
    {
		if (RING[0].at(k)>1)
		{
			// if there is a cargo at k
			if ( RING[2].at(k) > 0 )
			{
				// if there is no cago at k-1 or k+1 detachment possible.
				// otherwise detachment queue is not filled
				if (k-1 > 0 && k < RING[0].size()-1)
				{
					if (RING[2][k-1] < 1 && RING[2][k+1] < 1)
					{
						// detachment depending on GTP cap
						OFF.push_back(k);
					}
					else 
					{
						OFF2.push_back(k);
					}
				}
			}
			else
			{
				OFF.push_back(k);
			}

			if(RING[0][k+1]<1)
				DRIVE1.push_back(k);
		}
		else ON.push_back(k);
// Oligo kinetics
		if(RING[2][k]>0){
			for(int j=0; j<RING[2][k]; j++)
				OFFoligo.push_back(k);
		}
		if(RING[0][k]>1)
			ONoligo.push_back(k);
    }
	last_pos = RING[0].size()-1;

	// The following conditions concern the boundaries plus end
	// which need to be treated differently (omitted in loop above)
	if (RING[0][last_pos]<1)
		ON.push_back(last_pos);
	if(RING[2][last_pos]>0){
		for(int j=0; j<RING[2][last_pos]; j++)
			OFFoligo.push_back(last_pos);
	}
	if(RING[0][last_pos]>1)
		ONoligo.push_back(last_pos);

	// Creating all the propensities, i.e. overall rates of reactions which may occurr.
	RATES.clear();
	RATES.push_back(0.0);
	RATES.push_back(RATES.back() + speed1 * DRIVE1.size());
	RATES.push_back(RATES.back() + on * ON.size());
	RATES.push_back(RATES.back() + off * OFF.size());
	RATES.push_back(RATES.back() + onOLIGO * ONoligo.size());
	RATES.push_back(RATES.back() + offOLIGO * OFFoligo.size());
	RATES.push_back(RATES.back() + beta * RING[0][last_pos]/2.);
	RATES.push_back(RATES.back() + grow);
	RATES.push_back(RATES.back() + alpha * (1-RING[0][0]/2.));
	RATES.push_back(RATES.back() + off2 * OFF2.size());
	
	/* 
	The Gillespie Algorithm
	*/

	// Determine exponentially distributed timestep
	dt=log(1/gsl_rng_uniform_pos(r))/(RATES.back());
	Time += dt;
	
	// Choose which of the reactions should be carried out
	// Important to note is that the order has to maintained corresponding to the propensities in RATES[] container
	i=1;
	ran = gsl_rng_uniform_pos(r)*RATES.back();
	while (RATES.at(i)<ran) {i++;}
	if (i==1) {
		makeDRIVE1();
	}
	else if (i==2) {
		makeON();
	}
	else if (i==3) {
		makeOFF();
	}
	else if (i==4) {
		makeOLIGOon();
	}
	else if (i==5) {
		makeOLIGOoff();
	}
	else if (i==6) {
		makeTIPOFF();
	}
	else if (i==7) {
		makeGRO();
	}
	else if (i==8) {
		makeIN();
	}
	else if (i==9) {
		makeOFF2();
	}


	/*
	This section generates output for time dependent measurements.
	FLAG indicates if the system has been equilibrated and Clock sets first the equilibration time
	and then the fequency of data acquisition.
	*/
	if (FLAG > 0 && Time > Clock)
	{
		fstream file_tasep;
		char * DFile;
		DFile = new char[80];
		sprintf (DFile, "trjLK_den%f.dat", dens);
	    file_tasep.open(DFile, std::fstream::in | std::fstream::out | std::fstream::app);
		for (int k=0; k<RING[0].size(); k++) file_tasep << RING[0][k] << " ";
		file_tasep << "\n";
		file_tasep.close();
		delete DFile;

#if CARGO || OLIGO
		fstream file2_tasep;
		char * D2File;
		D2File = new char[80];
		sprintf (D2File, "trjTIP_den%f.dat", dens);
	    file2_tasep.open(D2File, std::fstream::in | std::fstream::out | std::fstream::app);
		for (int k=0; k<RING[2].size(); k++) file2_tasep << RING[2][k] << " ";
		file2_tasep << "\n";
		file2_tasep.close();
		delete D2File;
#endif

#if CAP
		fstream file3_tasep;
		char * D3File;
		D3File = new char[80];
		sprintf (D3File, "trjCAP_den%f.dat", dens);
	    file3_tasep.open(D3File, std::fstream::in | std::fstream::out | std::fstream::app);
		for (int k=0; k<RING[1].size(); k++) file3_tasep << RING[1][k] << " ";
		file3_tasep << "\n";
		file3_tasep.close();
		delete D3File;
#endif

		// Clock_count provides the time interval between recordings
		// In the analysis count is used to refer to time here (count * Clock_count, here count * 10).
		Clock=Clock+Clock_count;
		count++;
	}

	// If Time exceeds Clock equilibration has been reached.
	// The program will create a transfer event and continue with data recording.
	// If count exceeds MAX_count then the time limit for recording has been reached.
	// OLD if (Time > Clock  || count > MAX_count) return 0;
	if (Time > Clock || count >= MAX_count) return 0;
	else return 1; 
}

