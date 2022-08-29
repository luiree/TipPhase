/*
 *  bottleneck_ttrack7.h
 *  
 *  Created by Louis Reese on 24.08.10.
 *  Copyright 2020 Louis Reese. All rights reserved.
 *	
 *	Adapted for cargo clustering study.
 *	Time dependent phenomna.
 *
 */

#include <iostream>
#include <fstream>
#include <deque>
#include <iterator>
#include <gsl/gsl_rng.h>

class RING
{
public:
	///////
	// Initialise & Gets
	///////
	
	gsl_rng * r;
	
	void InitClass(char *parameters[]);
	void InitLanes(char *parameters[]);
	void InitLanesNoShock(char *parameters[]);
	void EquiLanes(char *parameters[]);
	void RngInit(char *parameters[]);
	
	long int RanInit;
	int i;
	
	int KIN(char *parameters[]);
	
	int Size, Number, stacksize;
	double speed,speed1,speed2,k1, hydr, grow, beta, beta1, on, off, off2, dens;
	double onCARG, offCARG, Kcarg, rhoCARG, CONC;
	double onOLIGO, offOLIGO, Koligo, rhoOLIGO;

private:
	int count, MAX_count, COUNTDATA;
	double dt, Time, Clock, Clock_count;
	double grow_time, free_time, depol_time, delta_time, diff_const, alpha, K, rho;
	double ran;
	int ran_int, position, last_pos;
	int FLAG;
	
	std::deque <double> RATES; //Propensity vector
	
	std::deque < std::deque <unsigned int > > RING; //current configuration of motors/nucleotide state/cargo
	std::deque <unsigned int> DRIVE1; //List of hopping particles on GDP lattice
	std::deque <unsigned int> DRIVE2; //List of hopping particles at the tip
	std::deque <unsigned int> HYDR; //List of GTP lattice
	std::deque <unsigned int> MATURE; //List of transition state lattice
	std::deque <unsigned int> ON; //List of free lattice sites for motor attachment
	std::deque <unsigned int> OFF; //List of motors detaching from GDP lattice
	std::deque <unsigned int> OFF2; //List of motors detaching from the MT cap
	std::deque <unsigned int> OFFcargo; //List of bound cargo particles
	std::deque <unsigned int> ONcargo; //List of cargo attachment sites  
	std::deque <unsigned int> ONoligo; //List of possible cargos for clustering
	std::deque <unsigned int> OFFoligo; //List of possible cargos for clustering

	unsigned int IN, OUT, GRO; 	// Variables to indicate entry and exit of motors
								// at the lattice boundaries and lattice growth.

	std::deque <unsigned int>::iterator it; // Iterator for working with the containers
	
	// System state update functions
	void makeDRIVE1();
	void makeDRIVE2();
	void makeHYDR();
	void makeMATURE();
	void makeON();
	void makeOFF();
	void makeOFF2();
	void makeTIPOFF();
	void makeOUT();
	void makeGRO();
	void makeIN();
	void makeCARGon();
	void makeCARGoff();
	void makeOLIGOon();
	void makeOLIGOoff();

};	

extern RING First;
