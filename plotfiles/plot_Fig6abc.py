# %%

# MIT License

# Copyright (c) 2022 luiree (Louis Reese)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import pandas as pd
from pylab import *
import string
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import matplotlib as mpl
import csv
import os
import sys
import re 

fig_width_pt = 320.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width *golden_mean      # height in inches


mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['legend.fontsize'] = 9
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['legend.labelspacing'] = 0.2
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['font.size'] = 10
mpl.rcParams['text.usetex'] = False

lattice_um=1000/8.4 # conversion factor lattice to um

### LOAD CARGO data

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)
#Path of parent directory
parentDirectory = os.path.dirname(fileDirectory)
#Navigate to Strings directory
Paths = os.path.join(parentDirectory, 'datafiles')   
print(Paths)

conditions = ["CAR1-OLI0-CAP0-CLUS0-DET0",
              "CAR1-OLI0-CAP1-CLUS0-DET0",
              "CAR1-OLI0-CAP0-CLUS1-DET0-off/off3",
              "CAR1-OLI0-CAP1-CLUS1-DET0-off/off3",
              "CAR1-OLI0-CAP1-CLUS1-DET1",
              "CAR1-OLI0-CAP0-CLUS1-DET1"]

conditions0 = ["CAR0-OLI1-CAP0-CLUS0-DET0",
              "CAR0-OLI1-CAP1-CLUS0-DET0",
              "CAR0-OLI1-CAP0-CLUS1-DET0-off/off3",
              "CAR0-OLI1-CAP1-CLUS1-DET0-off/off3",
              "CAR0-OLI1-CAP1-CLUS1-DET1",
              "CAR0-OLI1-CAP0-CLUS1-DET1"]

dens = ["0.004975",
        "0.009901",
        "0.014778",
        "0.019608",
        "0.024390",
        "0.029126",
        "0.033816",
        "0.038462",
        "0.043062"]

conc = ["20", "40", "60", "80", "100", "120", "140", "160", "180"]

df = pd.DataFrame(columns=['condition', 'rho', 'x', 'rho_motor', 'motor_density', 'cap', 'cap_density1', 'cap_density2'])
dfO = pd.DataFrame(columns=['condition', 'rho', 'x', 'rho_motor', 'motor_density', 'cap', 'cap_density1', 'cap_density2'])

cols=2
rows=4

m=4
for i in range(len(conditions)):
    fromfile = np.loadtxt(Paths+"/"+conditions[i]+"/trjTIP_den"+dens[m]+".dat.den", delimiter=" ")
    fromfile2 = np.loadtxt(Paths+"/"+conditions[i]+"/trjLK_den"+dens[m]+".dat.den", delimiter=" ")
    if "CAP1" in conditions[i]:
        fromfile3 = np.loadtxt(Paths+"/"+conditions[i]+"/trjCAP_den"+dens[m]+".dat.den1", delimiter=" ")
        fromfile4 = np.loadtxt(Paths+"/"+conditions[i]+"/trjCAP_den"+dens[m]+".dat.den2", delimiter=" ")
        data = {
            'condition': conditions[i], 
            'rho': np.asarray(fromfile.T[1]), 
            'x': np.asarray(fromfile.T[0]),
            'rho_motor' : np.asarray(fromfile2.T[1]),
            'motor_density' : np.zeros(len(fromfile.T[0]))+float(dens[m]),
            'cap' : True,
            'cap_density1' : np.asarray(fromfile3.T[1]),
            'cap_density2' : np.asarray(fromfile4.T[1])
        }
    else:
        data = {
            'condition': conditions[i], 
            'rho': np.asarray(fromfile.T[1]), 
            'x': np.asarray(fromfile.T[0]),
            'rho_motor' : np.asarray(fromfile2.T[1]),
            'motor_density' : np.zeros(len(fromfile.T[0]))+float(dens[m]),
            'cap' : False,
            'cap_density1' : np.zeros(len(fromfile.T[0])),
            'cap_density2' : np.zeros(len(fromfile.T[0]))
        }
        
    df = df.append(data, ignore_index=True)


    
for i in range(len(conditions0)):
    fromfile = np.loadtxt(Paths+"/"+conditions0[i]+"/trjTIP_den"+dens[m]+".dat.den", delimiter=" ")
    fromfile2 = np.loadtxt(Paths+"/"+conditions0[i]+"/trjLK_den"+dens[m]+".dat.den", delimiter=" ")
    if "CAP1" in conditions0[i]:
        fromfile3 = np.loadtxt(Paths+"/"+conditions0[i]+"/trjCAP_den"+dens[m]+".dat.den1", delimiter=" ")
        fromfile4 = np.loadtxt(Paths+"/"+conditions0[i]+"/trjCAP_den"+dens[m]+".dat.den2", delimiter=" ")
        data = {
            'condition': conditions0[i], 
            'rho': np.asarray(fromfile.T[1]), 
            'x': np.asarray(fromfile.T[0]),
            'rho_motor' : np.asarray(fromfile2.T[1]),
            'motor_density' : np.zeros(len(fromfile.T[0]))+float(dens[m]),
            'cap' : True,
            'cap_density1' : np.asarray(fromfile3.T[1]),
            'cap_density2' : np.asarray(fromfile4.T[1])
        }
    else:
        data = {
            'condition': conditions0[i], 
            'rho': np.asarray(fromfile.T[1]), 
            'x': np.asarray(fromfile.T[0]),
            'rho_motor' : np.asarray(fromfile2.T[1]),
            'motor_density' : np.zeros(len(fromfile.T[0]))+float(dens[m]),
            'cap' : False,
            'cap_density1' : np.zeros(len(fromfile.T[0])),
            'cap_density2' : np.zeros(len(fromfile.T[0]))
        }
        
    dfO = dfO.append(data, ignore_index=True)


fig=plt.figure(num=None, constrained_layout=False, figsize=(fig_width*1.0, 1.3*fig_height), dpi=300, facecolor='w', edgecolor='k')
# fig = plt.figure(constrained_layout=True, figsize=(cols*2 ,rows*4))
# spec = fig.add_gridspec(ncols=cols, nrows=rows)

# ax = fig.add_subplot(spec[0, 0])
# ax1 = fig.add_subplot(spec[1, 0])
# ax2 = fig.add_subplot(spec[2, 0])
# ax3 = fig.add_subplot(spec[3, 0])
ax03=fig.add_subplot(313)
ax01=fig.add_subplot(311, sharey=ax03)
ax02=fig.add_subplot(312, sharey=ax03)

# ax0 = fig.add_subplot(spec[0, 1])
# ax01 = fig.add_subplot(spec[1, 1])
# ax02 = fig.add_subplot(spec[2, 1])
# ax03 = fig.add_subplot(spec[3, 1])

ymax=[0.35, .35, .35, .35]
ymax0=[0.35, .35, .35, 0.35]

size_x = 1000
min_x = 1000-1*lattice_um
# ax.set_ylim(0,ymax[0])
# ax.set_xlim(min_x, size_x+1) #600-3*lattice_um
# ax.set_xticks([size_x,size_x-1*lattice_um,size_x-2*lattice_um])
# ax.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax.set_ylabel('Motor/Cargo occupation', fontsize=12)
 
# ax1.set_ylim(0,ymax[1])
# ax1.set_xlim(min_x, size_x+1) #600-3*lattice_um
# ax1.set_xticks([size_x,size_x-1*lattice_um,size_x-2*lattice_um])
# ax1.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax1.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax1.set_ylabel('Motor/Cargo occupation', fontsize=12)

# ax2.set_ylim(0,ymax[2])
# ax2.set_xlim(min_x, size_x+1) #600-3*lattice_um
# ax2.set_xticks([size_x,size_x-1*lattice_um,size_x-2*lattice_um])
# ax2.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax2.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax2.set_ylabel('Cargo occupation', fontsize=12)
 
# ax3.set_ylim(0,ymax[3])
# ax3.set_xlim(min_x, size_x+1) #600-3*lattice_um
# ax3.set_xticks([size_x,size_x-1*lattice_um,size_x-2*lattice_um])
# ax3.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax3.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax3.set_ylabel('Cargo occupation', fontsize=12)


# ax0.set_ylim(0,ymax0[0])
# ax0.set_xlim(min_x, size_x+1) #600-3*lattice_um
# ax0.set_xticks([size_x,size_x-1*lattice_um,size_x-2*lattice_um])
# ax0.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax0.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax0.set_ylabel('Motor/Cargo occupation', fontsize=12)



ax03.tick_params(direction="in", bottom=True, top=True, left=True, right=True)
ax01.tick_params(direction="in", bottom=True, top=True, left=True, right=True)
ax02.tick_params(direction="in", bottom=True, top=True, left=True, right=True)

ax03.set_ylim(0,ymax0[3])
ax03.set_yticks([0.0, 0.1, 0.2, 0.3])
ax03.set_yticklabels(['0', '0.1', '0.2', '0.3'])
ax03.set_xlim(min_x, size_x+1) #600-3*lattice_um
ax03.set_xticks([size_x,size_x-0.25*lattice_um, size_x-0.5*lattice_um,size_x-.75*lattice_um,size_x-1*lattice_um])
ax03.set_xticklabels(['0 $\mu$m','0.25 $\mu$m','0.5 $\mu$m','0.75 $\mu$m','1 $\mu$m'], fontsize=10)
ax03.set_xlabel('Distance from plus end ($\mu$m)', fontsize=10)
# ax03.set_ylabel('Cargo occupation', fontsize=10)


ax01.set_ylim(0,ymax0[1])
ax01.set_xlim(min_x, size_x+1) #600-3*lattice_um
ax01.set_yticks([0.0, 0.1, 0.2, 0.3])
ax01.set_yticklabels(['0', '0.1', '0.2', '0.3'])
ax01.set_xticks([size_x,size_x-0.25*lattice_um, size_x-0.5*lattice_um,size_x-.75*lattice_um,size_x-1*lattice_um])
ax01.set_xticklabels([])
# ax01.set_xlabel('Distance from plus end ($\mu$m)', fontsize=12)
# ax01.set_xlabel(None)
# ax01.set_xticklabels(None)
# ax01.set_ylabel('Motor/Cargo occupation', fontsize=12)
# ax01.tick_params(bottom=False) 

ax02.set_ylim(0,ymax0[2])
ax02.set_xlim(min_x, size_x+1) #600-3*lattice_um
ax02.set_yticks([0.0, 0.1, 0.2, 0.3])
ax02.set_yticklabels(['0', '0.1', '0.2', '0.3'])
ax02.set_xticks([size_x,size_x-0.25*lattice_um, size_x-0.5*lattice_um,size_x-.75*lattice_um,size_x-1*lattice_um])
ax02.set_xticklabels([])
# ax02.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
ax02.set_xlabel(None)
ax02.set_ylabel('Occupation probability', fontsize=10)


for k in [ 1 ]:  
    filt = dfO['condition'] == conditions0[k]
    cap1 = dfO[filt].cap_density1
    # ax1.plot(cap1.values[0],label="cap1")
    cap2 = dfO[filt].cap_density2
    lattice = dfO[filt].rho
    density_lattice = dfO[filt].motor_density
    
    curve_cap, = ax01.plot((cap2.values[0] + cap1.values[0])*0.3, '--', label="GTP cap (normalized)", color='0.5')
    curve_cargo, = ax01.plot(lattice.values[0],label="Cargo", color='darkorange') #conditions[k])
    motorlattice = dfO[filt].rho_motor
    curve_motor, = ax01.plot(motorlattice.values[0],'k-',label="Motor") #, color='green')
    # ax01.plot(density_lattice.values[0], '--', color='green',label="Theory motor")

    # for number in curve_cap.get_ydata()[int(min_x):]:
    #     print(float(number))
        
    # for number in curve_cargo.get_ydata()[int(min_x):]:
    #     print(float(number))
    
    # for number in curve_motor.get_ydata()[int(min_x):]:
    #     print(float(number))
    
ax01.legend(fontsize=9, fancybox=False, frameon=False,loc=2)

dummy=-5
# 5,4
for k in [ 5,4 ]:   
    filt = dfO['condition'] == conditions0[k]
    cond=["Cargo", "Cargo + cap"]
    lattice = dfO[filt].rho
    curve, = ax02.plot(lattice.values[0],label=cond[dummy+k])
    
    # for number in curve.get_ydata()[int(min_x):]:
    #     print(float(number))
    
    dummy=-3
    density_lattice = dfO[filt].motor_density
    # ax02.plot(density_lattice.values[0], '--',  label="Theory motor")
     
ax02.legend(fontsize=9, fancybox=False, frameon=False,loc=2)

for k in [ 2,3 ]:  
    filt = dfO['condition'] == conditions0[k]
    cond=["Cargo", "Cargo + cap"]
    lattice = dfO[filt].rho
    curve, = ax03.plot(lattice.values[0],label=cond[k-2])
    
    # for number in curve.get_ydata()[int(min_x):]:
    #     print(float(number))
    
    motorlattice = dfO[filt].rho_motor
    # ax03.plot(motorlattice.values[0], '-', label="Motor")
    density_lattice = dfO[filt].motor_density
    # ax03.plot(density_lattice.values[0], '--',color='green', label="Theory motor")
    
ax03.legend(fontsize=9, fancybox=False, frameon=False,loc=2)

subplots_adjust(left=0.15, bottom=0.15,right=0.95,top=0.95,wspace=0.0,hspace=0.1)


plt.show()


# %%
