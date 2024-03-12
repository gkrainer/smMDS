# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:43:17 2019

@author: RaphaelJacquat
"""
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import glob
import os
from matplotlib import cm
import matplotlib
import os.path
import re
from getBursts_fct import get_bursts, get_ptufilename
cmap = cm.viridis
plt.close("all")

# % parameters
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
user_setting = {"set_lee_filter": 2,
                "threshold_iT_signal": 0.05,
                "threshold_iT_noise": 0.1,
                "min_phs_burst" : 10,
                "min_phs_noise" : 160,
                "filter_name" : "addLeefilter",
                "show_plot" : False,
                "output_folder": "output"}
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

filename = get_ptufilename()

#extract all ptu in the folder of the file
filenames = glob.glob(os.path.join(os.path.dirname(filename),'*.ptu'))

outputfile_names = [name[:-3] + "out" for name in filenames]
numb_photons_files = np.zeros(len(filenames))
meanIntensities = np.zeros(len(filenames))
medianIntensities = np.zeros(len(filenames))
maxIntensities = np.zeros(len(filenames))
numb_photons_Total_files = np.zeros(len(filenames))
positions = np.zeros(len(filenames))
# %%
NI_list = ()
jj = 0  # iteration for the for loop, for each position, if count burst.retrieve
for filename, outputfile_name in zip(filenames, outputfile_names):
    #If outputfile  does not exist creats it with readPTU
    if not os.path.isfile(outputfile_name):
        readPTU(filename, outputfile_name)

    # Find the position in um within the filename and put it in positions
    # TODO -> force to generate metadata file retrieve position within .json
    str_pos = re.search( r'\_([0-9]{1,6}.[0-9]{0,2})?um\_', filename).group(1)
    positions[jj] = np.asarray(str_pos, dtype = float)
    print(str(jj)+' '+str(positions[jj]))



    photons_results, bursts_result = get_bursts(filename, user_setting)
    Photons = np.asarray(photons_results)
    NI = np.asarray(bursts_result["Burst intensity"])
    TBurst = np.asarray(bursts_result["Burst duration"])
    if NI.size > 0:
        numb_photons_files[jj] = np.size(NI)
        meanIntensities[jj] = np.nanmean(NI)
        medianIntensities[jj] = np.nanmedian(NI)
        maxIntensities[jj] = np.nanmax(NI)
    else:
        numb_photons_files[jj] = 0
    numb_photons_Total_files[jj] = Photons[:, 1].size

    jj = jj + 1
    NI_list = NI_list + (NI,)


# zipped_pairs = zip(positions, NI_list)
# NI_list = np.asarray([x for _, x in sorted(zipped_pairs)])
zipped_pairs = zip(positions, numb_photons_files)
numb_photons_files = np.asarray([x for _, x in sorted(zipped_pairs)])
zipped_pairs = zip(positions, numb_photons_Total_files)
numb_photons_Total_files = np.asarray([x for _, x in sorted(zipped_pairs)])
zipped_pairs = zip(positions, meanIntensities)
meanIntensities = np.asarray([x for _, x in sorted(zipped_pairs)])
zipped_pairs = zip(positions, medianIntensities)
medianIntensities = np.asarray([x for _, x in sorted(zipped_pairs)])
zipped_pairs = zip(positions, maxIntensities)
maxIntensities = np.asarray([x for _, x in sorted(zipped_pairs)])
positions = sorted(positions)
#%%
fig = plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.plot(positions, numb_photons_files)
plt.legend(['Single molecule detection'])

ax1 = plt.gca()
ax2 = ax1.twinx()
ax2.plot(positions[:-1], numb_photons_Total_files[:-1], '--', c="C1")
ax1.set_ylabel('Number of Molecule',color="C0")
ax2.set_ylabel('Intensity [a.u.]', color="C1")
plt.legend(['Total number photon'])
ax1.set_xlabel('channels crosssection [um]')
plt.title(f'Parameter: minPhs = {user_setting["min_phs_burst"]}, minPhsN = {user_setting["min_phs_noise"]}')
# plt.legend(('Single molecule detection','(sum of photon -11600) / 100'))
plt.subplot(1,2,2)
plt.semilogy(positions, numb_photons_files)
plt.legend(['Single molecule detection'])
ax1 = plt.gca()
ax2 = ax1.twinx()
ax2.semilogy(positions[:-1], numb_photons_Total_files[:-1], '--', c="C1")
plt.legend(['Total number photon'])
ax1.set_ylabel('Number of Molecule',color="C0")
ax2.set_ylabel('Intensity [a.u.]', color="C1")
ax1.set_xlabel('channels crosssection [um]')
fig.tight_layout()
# plt.savefig(filename[:-filename.find('\\')]+"sum_singlemolecule_0.05.pdf")
#%%
plt.figure()
colors = (medianIntensities - np.nanmin(medianIntensities))
if len(colors) != 0:
    colors = colors / np.nanmax(colors) * 255
for i in np.arange(0,medianIntensities.size):
    plt.plot(positions[i], numb_photons_files[i],
             'o', color = cmap.colors[int(colors[i])])
#%%
dirname = os.path.dirname(filename)
output_foldername = os.path.join(dirname ,
                                 user_setting["output_folder"])
np.savetxt(os.path.join(output_foldername,
                        "Analysed_data_positions.txt"),
           positions,
           delimiter=',')
np.savetxt(os.path.join(output_foldername,
                        "Analysed_data_numb_molecules.txt"),
           numb_photons_files,
           delimiter=',')
# np.savetxt(os.path.join(output_foldername,
#                         "Analysed_data_meanIntensities.txt"),
#            meanIntensities,
#            delimiter='')
# np.savetxt(os.path.join(output_foldername,
#                         "Analysed_data_medianIntensities.txt"),
#            medianIntensities,
#            delimiter='')
# np.savetxt(os.path.join(output_foldername,
#                         "Analysed_data_maxIntensities.txt"),
#            maxIntensities,
           delimiter='')
np.savetxt(os.path.join(output_foldername,
                        "Analysed_data_SumPhoton.txt"),
           numb_photons_Total_files,
           delimiter='')
np.savetxt(os.path.join(output_foldername,
                        "Analysed_data_inputparameter.txt"),
           np.asarray([user_setting[x] for x in user_setting.keys()],dtype=str),
           delimiter=',',
           fmt="%s")

positions = np.asarray(positions)
positions = positions.reshape((1, np.size(positions)))
numb_photons_files = numb_photons_files.reshape((
                                               1, np.size(numb_photons_files)
                                               ))
meanIntensities = meanIntensities.reshape((1, np.size(meanIntensities)))
medianIntensities = medianIntensities.reshape((1, np.size(medianIntensities)))
maxIntensities = maxIntensities.reshape((1, np.size(maxIntensities)))
numb_photons_Total_files = numb_photons_Total_files.reshape((1, np.size(numb_photons_Total_files)))

concatenatefile = np.concatenate([positions.T,
                                  numb_photons_files.T,
                                  meanIntensities.T,
                                  medianIntensities.T,
                                  maxIntensities.T,
                                  numb_photons_Total_files.T
                                  ],
                                  axis=1)
np.savetxt(os.path.join(output_foldername,"Alldata.txt"), concatenatefile, delimiter=',')



