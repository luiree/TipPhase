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
from matplotlib import cm
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


mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['legend.labelspacing'] = 0.2
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['font.size'] = 8
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

conditions0 = ["CAR0-OLI1-CAP0-CLUS0-DET0",
              "CAR0-OLI1-CAP1-CLUS0-DET0",
              "CAR0-OLI1-CAP0-CLUS1-DET0-off/off3",
              "CAR0-OLI1-CAP1-CLUS1-DET0-off/off3",#3
              "CAR0-OLI1-CAP1-CLUS1-DET1",#4
              "CAR0-OLI1-CAP0-CLUS1-DET1",
              "CAR0-OLI1-CAP1-CLUS1-DET0-off/off5",#6
              "CAR0-OLI1-CAP1-CLUS1-DET0-off/off7",#7
              "CAR0-OLI1-CAP1-CLUS1-DET0-off/off9"
              ]

dens = ["0.000250",
        "0.001248",
        "0.002494",
        "0.004975",
        "0.009901",
        "0.014778",
        "0.019608",
        "0.024390",
        "0.029126",
        "0.033816",
        "0.038462",
        "0.043062",
        "0.047619",
        "0.052133",
        "0.056604",
        "0.061033",
        "0.065421",
        "0.069767",
        "0.074074",
        "0.078341",
        "0.082569",
        "0.086758",
        "0.090909",
        "0.095023",
        "0.099099",
        "0.103139",
        "0.107143",
        "0.111111",
        "0.115044",
        "0.118943",
        "0.122807",
        "0.126638",
        "0.130435",
        "0.134199",
        "0.137931",
        "0.141631",
        "0.145299",
        "0.148936"]

conc = ["1", "5", "10", "20", "40", "60", "80", "100", "120", "140", "160", "180",
        "200", "220", "240", "260", "280", "300", "320", "340", "360", "380", "400",
        "420", "440", "460", "480", "500", "520", "540", "560", "580", "600", 
        "620", "640", "660", "680", "700"]

dfO = pd.DataFrame(columns=['condition', 'rho', 'x', 'rho_motor', 'motor_density', 'cap', 'cap_density1', 'cap_density2'])


for m in range(len(conc)):    
    for i in [3,4,6,7,8]: #range(len(conditions0)):
        fromfile = np.loadtxt(Paths+"/"+conditions0[i]+"/trjTIP_den"+dens[m]+".dat.den", delimiter=" ")
        fromfile2 = np.loadtxt(Paths+"/"+conditions0[i]+"/trjLK_den"+dens[m]+".dat.den", delimiter=" ")
        if "CAP1" in conditions0[i]:
            data = {
                'condition': conditions0[i], 
                'rho': np.asarray(fromfile.T[1]), 
                'x': np.asarray(fromfile.T[0]),
                'rho_motor' : np.asarray(fromfile2.T[1]),
                'motor_density' : np.zeros(len(fromfile.T[0]))+float(dens[m]),
                'conc' : float(conc[m]),
                'cap' : True,
                # 'cap_density1' : np.asarray(fromfile3.T[1]),
                # 'cap_density2' : np.asarray(fromfile4.T[1])
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
                # 'cap_density1' : np.zeros(len(fromfile.T[0])),
                # 'cap_density2' : np.zeros(len(fromfile.T[0]))
            }
            
        dfO = dfO.append(data, ignore_index=True)


# fig=plt.figure(num=None, constrained_layout=False, figsize=(fig_width*1.8, 0.6*fig_height), dpi=300, facecolor='w', edgecolor='k')

# ax1=fig.add_subplot(131)
# ax0=fig.add_subplot(132)
# ax2=fig.add_subplot(133)
# subplots_adjust(left=0.10, bottom=0.17,right=0.99,top=0.95,wspace=0.410,hspace=0.1)

# ymax=[0.35, .35, .35, .35]
# ymax0=[0.35, .35, .35, .35]


# ax0.tick_params(reset=True,axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)
# ax0.set_xlabel('Motor concentration (nM)')
# ax0.set_ylabel('Fold change tip/lattice')

# ax2.tick_params(reset=True,axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)
# ax2.set_xlabel('Motor concentration (nM)')
# ax2.set_ylabel('Mean cargo occupation \n Tip & lattice (symbols w edge)')


col=['green','red','purple','blue','darkorange','black','darkgreen','yellow', 'yellow','yellow']
delta= 12 #round(lattice_um/12)
delta2= 119 #round(lattice_um/12)
pos_lattice = 869-119
pos_all=1000

# labels = ["a","b","x","$k_{off}^c=0.027\,\mathrm{sec}^{-1}$","$k_{off}^c=0.08\,\mathrm{sec}^{-1}$","c","$k_{off}^c=0.0053\,\mathrm{sec}^{-1}$","$k_{off}^c=0.000085\,\mathrm{sec}^{-1}$","$k_{off}^c=0.004\,\mathrm{sec}^{-1}$"]

# mark = [">","-","-","o","s","-","d","d","d"]

# for cond in [7,6,3,4]: 
#     line_plot_dataO = []
#     for k in range(len(conc)):
#         filtO = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
#         latticeO = dfO[filtO].rho
#         AO=np.mean(latticeO.values[0][1000-delta:1000])
#         A2O=np.mean(latticeO.values[0][pos_lattice-2*delta2:pos_lattice-delta2])
#         if k==0:
#             ax0.scatter(conc[k],AO/A2O,color=col[cond], marker=mark[cond],label=labels[cond])
#             line_plot_dataO.append(AO/A2O)
#         else:
#             ax0.scatter(conc[k],AO/A2O,color=col[cond], marker=mark[cond])
#             line_plot_dataO.append(AO/A2O)

# ax0.set_xticks([conc[0], conc[12], conc[22], conc[32]])

# lstyle=['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-']
# alph=[0.0,0.0,0.0,1.0,1.0,0.0,1.0,1.0,1.0]
# labels = ["a","b","x","$k_{off}^c=0.027\,\mathrm{sec}^{-1}$","$k_{off}^c=0.08\,\mathrm{sec}^{-1}$","c","$k_{off}^c=0.0053\,\mathrm{sec}^{-1}$","$k_{off}^c=0.00085\,\mathrm{sec}^{-1}$","$k_{off}^c=0.004\,\mathrm{sec}^{-1}$"]

# size_x = 1000
# min_x = 1000-3*lattice_um

# delta2= 119 #round(lattice_um/12)
# pos_lattice = 869

# min_x = (pos_lattice-2*delta2)
# ax1.tick_params(axis="both",direction="in", bottom=True, top=True, left=True, right=True)
# ax1.set_xlim(size_x-3*lattice_um, size_x+1) #600-3*lattice_um
# ax1.set_xticks([size_x,size_x-1.*lattice_um,size_x-2.0*lattice_um,size_x-3.0*lattice_um])
# ax1.set_xticklabels(['0 $\mu$m','1 $\mu$m','2 $\mu$m','3 $\mu$m'])
# ax1.set_xlabel('Distance from plus end ($\mu$m)')
# ax1.set_ylabel('Mean cargo occupation')
# ax1.set_ylim([0,2.75])

# for cond in [7,6,3,4]:
#     for k in range(len(conc)):  
#         filt = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
#         lattice = dfO[filt].rho

#         white_transp = (1,1,1,0)
#         A=lattice.values[0][pos_lattice-delta2:-1]
#         Aall=lattice.values[0][:]
#         if k==0:
#             ax1.plot(Aall,color=col[cond],alpha=alph[cond], label=labels[cond], linestyle=lstyle[cond], linewidth=.8)
         
#         ax1.plot(Aall,color=col[cond],alpha=alph[cond], linestyle=lstyle[cond], linewidth=.8)
#         ax1.axvspan(size_x-3*lattice_um, size_x-2*lattice_um, facecolor='0.9', alpha=0.8)
#         ax1.axvspan(size_x-delta, size_x, facecolor='0.9', alpha=0.8)
        
    
# ax1.legend(fontsize=8, fancybox=True, frameon=True)


# for cond in [7,6,3,4]: 
#     line_plot_dataO = []
#     line_plot_data2O = []
#     for k in range(len(conc)):
#         filtO = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
#         latticeO = dfO[filtO].rho
#         AO=np.mean(latticeO.values[0][1000-delta:1000])
#         A2O=np.mean(latticeO.values[0][pos_lattice-2*delta2:pos_lattice-delta2])
#         if k==0:
#             ax2.scatter(conc[k],AO, color=col[cond], marker=mark[cond],label=labels[cond] , s=12)
#             line_plot_dataO.append(AO)
#             ax2.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=12)
#             line_plot_data2O.append(A2O)
#         else:
#             ax2.scatter(conc[k],AO, color=col[cond], marker=mark[cond], s=12)
#             line_plot_dataO.append(AO)
#             ax2.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=12)
#             line_plot_data2O.append(A2O)

#     conc_float = [float(i) for i in conc]
#     a = np.asarray([ conc_float, line_plot_dataO, line_plot_data2O ])
    
#     filename_csv="datapoints_sim_" + col[cond] + ".csv"
#     np.savetxt(filename_csv, np.round(np.transpose(a), decimals=8), fmt='%.8f', delimiter=",", header="concentration, tip, lattice")
#     ax2.set_xticks([conc[0], conc[12], conc[22], conc[32]])

# ax2.tick_params(reset=True,axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)
# ax2.set_xlabel('Motor concentration (nM)')
# ax2.set_ylabel('Mean cargo occupation')


# Figure 6f
fig2=plt.figure(num=None, constrained_layout=False, figsize=(fig_width*0.6, 0.6*fig_height), dpi=300, facecolor='w', edgecolor='k')

ax0=fig2.add_subplot(111)

subplots_adjust(left=0.15, bottom=0.17,right=0.85,top=0.95,wspace=0.410,hspace=0.1)

for cond in [7,6,3,4]: 
    line_plot_dataO = []
    line_plot_data2O = []
    for k in range(len(conc)):
        filtO = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
        # print(filtO)
        # print(dfO)
        latticeO = dfO[filtO].rho
        # print(k, size(latticeO.values[0]))
        AO=np.mean(latticeO.values[0][1000-delta:1000])
        A2O=np.mean(latticeO.values[0][pos_lattice-2*delta2:pos_lattice-delta2])
        if k==0:
            # ax2.scatter(conc[k],AO, color=col[cond], marker=mark[cond],label=labels[cond] , s=12)
            line_plot_dataO.append(AO)
            # ax2.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=12)
            line_plot_data2O.append(A2O)
        else:
            # ax2.scatter(conc[k],AO, color=col[cond], marker=mark[cond], s=12)
            line_plot_dataO.append(AO)
            # ax2.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=12)
            line_plot_data2O.append(A2O)
    # ax2.plot(conc, line_plot_dataO, color=col[cond],ls=('dashed'))

for cond in [3,4]: 
    line_plot_dataO = []
    line_plot_data2O = []
    for k in range(len(conc)):
        filtO = (dfO['conc'] == float(conc[k])) & (dfO['condition'] == conditions0[cond])
        # print(filtO)
        # print(dfO)
        latticeO = dfO[filtO].rho
        # print(k, size(latticeO.values[0]))
        AO=np.mean(latticeO.values[0][1000-delta:1000])
        A2O=np.mean(latticeO.values[0][pos_lattice-2*delta2:pos_lattice-delta2])
        if k==0:
            # ax0.scatter(conc[k],AO, color=col[cond], marker=mark[cond],label=labels[cond] , s=1)
            line_plot_dataO.append(AO)
            # ax0.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=1)
            line_plot_data2O.append(A2O)
        else:
            # ax0.scatter(conc[k],AO, color=col[cond], marker=mark[cond], s=1)
            line_plot_dataO.append(AO)
            # ax0.scatter(conc[k],A2O, color=col[cond], edgecolor='0', marker=mark[cond], s=1)
            line_plot_data2O.append(A2O)
    # ax2.plot(conc, line_plot_dataO, color=col[cond],ls=('dashed'))
    A = [float(x) for x in conc]
    ax0.plot(A[0:18], line_plot_dataO[0:18], color=col[cond],ls=('solid'))
    ax0.plot(A[0:18], line_plot_data2O[0:18], color=col[cond],ls=('dashed'))


    conc_float = [float(i) for i in conc]
    a = np.asarray([ conc_float, line_plot_dataO, line_plot_data2O ])
    # fmt = ",".join(["%10.6e"] * (a.shape[1]+1))
    
    filename_csv="fig6f_conditioncode_" + col[cond] + ".csv"
    np.savetxt(filename_csv, np.round(np.transpose(a), decimals=8), fmt='%.8f', delimiter=",", header="motor concentration, cargo occupation tip, cargo occupation lattice")

ax0.tick_params(reset=True,axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)
ax0.set_xlabel('Motor concentration (nM)')
ax0.set_ylabel('Cargo occupation')
ax0.set_xticks([0, 100, 200, 300])
ax0.set_xticklabels(["0", "100", "200", "300"])
ax0.set_ylim([0, 1.5])
ax0.set_xlim([0, 300])

# Drawing legend
ax0.plot(-1*A[0:18], -1*line_plot_dataO[0:18], color='black', ls=('solid'), label='microtubule tip')
ax0.plot(-1*A[0:18], -1*line_plot_data2O[0:18], color='black', ls=('dashed'), label='microtubule lattice')
handles, labels = ax0.get_legend_handles_labels()
print(ax0.get_legend_handles_labels())
ax0.legend(handles=(handles[0], handles[1]), loc='upper left')


plt.show()


# %%
