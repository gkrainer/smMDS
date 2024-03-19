# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:43:17 2019

@author: RaphaelJacquat

This Version is adapted from Matlab files of Andreas Hartmann given by Georg Krainer, several modification as been added by me
In order to run the files you will need different dependancies
readPTU, burstLoc, leeFilter


The Lee Filter of Matlab does not make anything than a moving average
The one which has been rewriten does a LeeFilter multiplicatif or additif, but
Personaly does not know why this filter is required or better.
Futur implementation should add moving average or Savgol filter.
"""

from scripts.Leefilter import leeFilter1D_matlab, leeFilter1D_Add
from scripts.burstLoc import burstLoc
from scripts.readPTU import readPTU
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os.path

root = tk.Tk()
# root.withdraw()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Parameters (Feel free to modify)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
setLeeFilter = 4
threIT = 0.05  # (ms) maximum inter-photon time signal (0.05)
threIT2 = 0.1  # (ms) minimum inter-photon time noise (0.05)
minPhs = 10  # minimum number of photons per burst (30)
minPhsN = 100  # minimum number of photons per noise region (60)
boolShow = 1

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Load data
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Open a windows to open PTU files.
filename = filedialog.askopenfilename(filetypes=(('ptu files', 'ptu'),))
root.withdraw()

outputfile_name = filename[:-3] + "out"
# Transform the binary data ".ptu" in readable data ".out" using readPTU
if not os.path.isfile(outputfile_name):
    readPTU(filename, outputfile_name)

#save data inside Photons variable which is an array of [Channel, time]
Photons = np.fromfile(outputfile_name)  # time save in (ps)
Photons = np.reshape(Photons, (-1, 2))
Photons[:, 1] = Photons[:, 1] / 1000  # time in ns : ps/1000 -> ns

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %% Find burst
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
macroT = Photons[:, 1]  # (ns)
channel = Photons[:, 0]

# find inter-photon time
interPhT = np.diff(macroT)  # (ns)
interLee = leeFilter1D_Add(interPhT, setLeeFilter)

# 1st filter
# threshold for inter photon time
indexSig = np.asarray(np.where(np.logical_and(0.4 < interLee,
                                              interLee < (threIT * 1000000))),
                      dtype=int)
# indexSig = np.where(0.4 < interLee )  # TODO add the logical end
indexSigN = np.asarray(np.where(interLee > (threIT2 * 1000000)))

if np.asarray(indexSig).size != 0:
    bStart, bLength = burstLoc(indexSig, 1)
    # bStartN, bLengthN = burstLoc(indexSigN, 1)

    # 2nd filter
    # minimum photons per burst

    bStartLong = bStart[bLength >= minPhs]
    bLengthLong = np.asarray(bLength[bLength >= minPhs], dtype=int)

    # bStartLongN = bStartN[bLengthN >= minPhsN]
    # bStartLongN = np.asarray(bStartLongN, dtype=int)
    # bLengthLongN = bLengthN[bLengthN >= minPhsN]
    # bLengthLongN = np.asarray(bLengthLongN, dtype=int)

    # collect Photons
    Bursts = np.zeros((int(np.sum(bLengthLong)), 3))
    lInd = 0

    for i in range(0, np.size(bStartLong)):

        BurstNumber = (np.ones(bLengthLong[i]) * i)
        Photons2 = Photons[
                           bStartLong[i]:
                           (bStartLong[i] + bLengthLong[i])
                           ]

        Bursts[lInd:lInd+bLengthLong[i], :] = np.concatenate((
                                                BurstNumber[:, np.newaxis],
                                                Photons2), axis=1)
        lInd = lInd + bLengthLong[i]

    BackN = 0
    BackT = 0

    # for i in range(0, np.size(bStartLongN)):

    #     GapPhotons = Photons[
    #                          bStartLongN[i]:
    #                          bStartLongN[i] + bLengthLongN[i]
    #                          ]

    #     BackT = BackT + GapPhotons[-1, 1] - GapPhotons[0, 1]

    #     BackN = BackN + np.size(GapPhotons)

    if BackT != 0:
        BI = BackN / BackT * 1e6
    else:
        BI = 0

    # separate all number of photons
    NI = np.zeros(np.size(bStartLong))
    TBurst = np.zeros(np.size(bStartLong))

    for i in range(0, np.size(bStartLong)):

        N = Bursts[Bursts[:, 0] == i, 2]
        NI[i] = np.size(N[:])

        TBurst[i] = np.sum(interPhT[bStartLong[i] - 1: bStartLong[i]
                           + bLengthLong[i] - 1] * 1e-6)  # (ms)

 # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %% Plot the different value
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if boolShow == 1:

#      #% show intensity time trace
        edges = np.arange(0, (np.round(macroT[-1] * 1e-6)))
        hI = np.histogram(macroT * 1e-6, edges)

        f1 = plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot((edges[:-1]+edges[0]/2) / 1000, hI[0])  # ps / 1000 = ns
        plt.xlim((0, 5))
        plt.xlabel('Time (s)')
        plt.ylabel('Count rate (kHz)')


        for i in range(0, np.size(bStartLong) - 1):
            masksup = macroT > macroT[bStartLong[i]]
            maskinf = macroT < macroT[bStartLong[i] + bLengthLong[i] + 1]
            mask = maskinf * masksup
            hI_red = np.histogram(macroT[mask] * 1e-6, edges)
            plt.plot((edges[:-1][hI_red[0] > 0] + edges[0]/2) / 1000,
                     hI_red[0][hI_red[0] > 0],
                     'rx-')

#      #% show inter-photon time
        plt.subplot(2, 2, 2)
        plt.plot(interPhT/1000000)
        plt.xlim((0, 1000))
        plt.xlabel('Photon$_{i+1->i}$')
        plt.ylabel('Inter-photon time (ms)')

        # for i in range(0, np.size(bStartLongN) - 1):

        #     plt.plot(np.arange(bStartLongN[i] + 1,
        #                        bStartLongN[i] + bLengthLongN[i]),
        #              interPhT[bStartLongN[i] + 1: bStartLongN[i] +
        #                       bLengthLongN[i]] / 1000000,
        #              'g')

        for i in range(0, np.size(bStartLong) - 1):

            plt.plot(np.arange(bStartLong[i] + 1,
                               bStartLong[i] + bLengthLong[i]),
                     interPhT[bStartLong[i] + 1: bStartLong[i] +
                              bLengthLong[i]] / 1000000,
                     'r')

#      #% show burst duration histogram
        edgesT = np.arange(0, 6, 0.1)
        hT = np.histogram(TBurst, edgesT)

        plt.subplot(2, 2, 3)
        plt.bar(edgesT[0:-1] + edgesT[1]/2, hT[0], edgesT[1])
        plt.xlabel('$T_{\mathrm{B}} $(ms)')
        plt.ylabel('Number of molecules')

#      #% show burst duration histogram
        edgesN = np.arange(0, 200, 5)
        edgesN = edgesN + edgesN[0]/2
        hN = np.histogram(NI, edgesN)

        plt.subplot(2, 2, 4)
        plt.bar(edgesN[0:-1]+edgesN[1]/2, hN[0], edgesN[1])
        plt.xlabel('$N$ Number of photons for one molecule')
        plt.ylabel('Number of molecules')
