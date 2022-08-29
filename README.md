# TipPhase

Hi!

TipPhase is a collection of code and data that I created to study enzymatic processes and phase separation phenomena that may occur at the tips of microtubules.

Some of the results are on the biorxiv and about to be published as "Multivalent interactions facilitate motor-dependent protein accumulation at growing microtubule plus ends" by Renu Maan, Louis Reese, Vladimir A. Volkov, Matthew R. King, Eli van der Sluis, Nemo Andrea, Wiel Evers, Arjen J. Jakobi, Marileen Dogterom. Read it here: https://www.biorxiv.org/content/10.1101/2021.09.14.460284v2 .

This repository also contains data that had been produced and python scripts for reproducing the plots in Figure 6 of the publication. 
You also will find bash scripts to automate cluster runs and to facilitate the analysis. 

Random numbers for stochastic simulations are generated using the GNU Scientific Library 2.6 (find it here for example https://ftp.gnu.org/gnu/gsl/). Make sure to install it before you start, or modify towards your preferred random number generator.

There is no guarantee this code will work in your environment. I used g++ 7.5.0 from the GCC on Ubuntu 18.04 and custom bash scripts to compile and generate different versions of the code.

Kind regards, 
Louis
