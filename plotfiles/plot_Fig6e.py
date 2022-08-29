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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from pylab import *
import string
from matplotlib.ticker import *
import matplotlib as mpl
# import matplotlib.gridspec as gridspec 
import os
import re 
import sys

fig_width_pt = 320.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width *golden_mean      # height in inches


mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['legend.fontsize'] = 8
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

for m in range(len(conc)):
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
                'conc' : float(conc[m]),
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
                'conc' : float(conc[m]),
                'cap' : False,
                'cap_density1' : np.zeros(len(fromfile.T[0])),
                'cap_density2' : np.zeros(len(fromfile.T[0]))
            }
            
        df = df.append(data, ignore_index=True)


for m in range(len(conc)):    
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
                'conc' : float(conc[m]),
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
                'conc' : float(conc[m]),
                'cap' : False,
                'cap_density1' : np.zeros(len(fromfile.T[0])),
                'cap_density2' : np.zeros(len(fromfile.T[0]))
            }
            
        dfO = dfO.append(data, ignore_index=True)





fig=plt.figure(num=None, constrained_layout=False, figsize=(fig_width*1.2, 0.6*fig_height), dpi=300, facecolor='w', edgecolor='k')

ax1=fig.add_subplot(121)
# ax0=fig.add_subplot(122)
subplots_adjust(left=0.10, bottom=0.17,right=0.99,top=0.95,wspace=0.410,hspace=0.1)

ax1.tick_params(axis="both",direction="in", bottom=True, top=True, left=True, right=True)

ymax=[0.35, .35, .35, .35]
ymax0=[0.35, .35, .35, .35]

size_x = 1000
min_x = 1000-3*lattice_um

delta2= 119 #round(lattice_um/12)
pos_lattice = 869

min_x = (pos_lattice-delta2)
size_x = 1000-min_x
ax1.set_xlim(0, size_x+1) #600-3*lattice_um
ax1.set_xticks([size_x,size_x-1.*lattice_um,size_x-2.0*lattice_um])
ax1.set_xticklabels(['0 $\mu$m','1.0 $\mu$m','2 $\mu$m'])
ax1.set_xlabel('Distance from plus end ($\mu$m)')
ax1.set_ylabel('Cargo occupation')
ax1.set_ylim([0,0.85])
ax1.set_yticks([0,0.2,0.4,0.6,.80])
ax1.set_yticklabels(['0','0.2','0.4','0.6','0.8'])

# ax0.tick_params(reset=True,axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)
# ax0.set_xlabel('Motor concentration (nM)')
# ax0.set_ylabel('Fold change tip/lattice')
# ax0.set_xticks([20, 60, 100, 140, 180])
# ax0.set_xticklabels(['20', '60', '100', '140', '180'])



col=['green','red','purple','blue','darkorange','black']
delta= 24 #round(lattice_um/12)
delta2= 119 #round(lattice_um/12)
pos_lattice = 869
pos_all=1000

labels = ["No cap, no cluster","Cap","x","Cap + cluster + stable","Cap + cluster"]
mark = [">","-","-","o","s"]
# for cond in [3,4,0]:
#     line_plot_data = []
#     line_plot_dataO = []
#     for k in [0,2,4,6,8]: #range(len(conc)):
#         filtO = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
#         latticeO = dfO[filtO].rho
#         AO=np.mean(latticeO.values[0][1000-delta:1000])
#         A2O=np.mean(latticeO.values[0][pos_lattice-delta2:pos_lattice])
#         if k==0:
#             ax0.scatter(conc[k],AO/A2O,color=col[cond], marker=mark[cond],label=labels[cond])
#             line_plot_dataO.append(AO/A2O)
#         else:
#             ax0.scatter(conc[k],AO/A2O,color=col[cond], marker=mark[cond])
#             line_plot_dataO.append(AO/A2O)
#     # ax0.plot(conc, line_plot_dataO,color=col[cond],ls=('dashed'))
# ax0.legend(fontsize=8, fancybox=True, frameon=True, loc=4)

lstyle=['-','-','-','-','-','-','-','-','-']
lstyle=['-','-','-','-','-','-','-','-','-']
alph=[0.0,0.0,0.0,1.0,1.0,0.0]
labels = ["a","b","x","$k_{off}=0.027\mathrm{sec}^{-1}$","$k_{off}=0.08\mathrm{sec}^{-1}$"]

for cond in [3, 4]: #34
    for k in [0,2,4,6,8]:  #02468
        filt = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
        lattice = dfO[filt].rho

        white_transp = (1,1,1,0)
        A=lattice.values[0][pos_lattice-delta2:-1]
        if k==0:
            ax1.plot(A,color=col[cond],alpha=alph[cond], label=labels[cond], linestyle=lstyle[cond], linewidth=.8)
         
        curve, = ax1.plot(A,color=col[cond],alpha=alph[cond], linestyle=lstyle[cond], linewidth=.8)
        ax1.axvspan(0, delta2, facecolor='0.9', alpha=0.8)
        ax1.axvspan(A.size-delta, A.size, facecolor='0.9', alpha=0.8)
        
    
    
ax1.legend(fontsize=8, fancybox=True, frameon=True)


plt.show()


# %%
