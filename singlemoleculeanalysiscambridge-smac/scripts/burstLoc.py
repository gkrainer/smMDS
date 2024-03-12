# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 13:01:44 2019

@author: RaphaelJacquat
"""
import numpy as np


def burstLoc(Arr, mindistance):
    """
    Localisation of the different burstLoc.

    Takes as argument the array (Arr) and the minimum distance (mindistance).
    Return the bStartAcc and bLengthAcc
    """
    Arr = np.append(Arr, Arr[0][-1])

    bIndex = np.asarray(np.where((Arr[1:] - Arr[:-1]) > 1)) + 1

    bIndex = np.insert(bIndex, 0, 0)
    bLength = np.zeros(np.size(bIndex))
    bStart = Arr[bIndex]

    for i in range(0, np.size(bIndex) - 1):

        length = 1
        index = bIndex[i]
        while Arr[index + 1] == (Arr[index] + 1):
            length = length + 1
            index = index + 1

        bLength[i] = length

    bStartAcc = bStart[0]
    bLengthAcc = bLength[0]

    for i in range(1, np.size(bStart) - 1):

        if (bStart[i]-(bStart[i-1] + bLength[i-1] - 1)) > mindistance:
            bStartAcc = np.append(bStartAcc, bStart[i])
            bLengthAcc = np.append(bLengthAcc, bLength[i])

    return bStartAcc, bLengthAcc
