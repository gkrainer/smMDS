# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:22:56 2019

@author: RaphaelJacquat
"""

import numpy as np
from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance


def leeFilter1D_Add(I, window_size):
    """
    Additif implementation of Lee filter

    Where I is the signa and windows_size the number of pixel take into account
    for the local mean
    output = localmean + K * (I - localmean)
    """

    I = np.array(I);
    mean_I = uniform_filter(I, (window_size))
    sqr_mean_I = uniform_filter(I**2, (window_size))
    var_I = sqr_mean_I - mean_I ** 2

    overall_variance = variance(I)

    weight_I = var_I / (var_I + overall_variance)
    output_I = mean_I + weight_I * (I - mean_I)
    return output_I


def leeFilter1D_Multi(I, window_size):
    """
    Multiplicatif implementation of Lee filter

    Where I is the signa and windows_size the number of pixel take into account
    for the local mean
    """

    I = np.array(I)
    mean_I = uniform_filter(I, (window_size))
    sqr_mean_I = uniform_filter(I**2, (window_size))
    var_I = sqr_mean_I - mean_I ** 2

    weight_I = (np.mean(I) * var_I /
                (mean_I ** 2 / window_size + (var_I * np.mean(I) ** 2)))
    output_I = mean_I + weight_I * (I - mean_I * np.mean(I))
    return output_I


def leeFilter1D_matlab(I, window_size):

    I = np.array(I)
    OIm = I
    means = uniform_filter(I, (window_size))
    sigmas = np.sqrt((I - means) ** 2 / window_size ** 2)
    sigmas = uniform_filter(sigmas, (window_size))

    ENLs = (means / sigmas) ** 2
    sx2s = ((ENLs * (sigmas) ** 2) - means ** 2) / (ENLs + 1)
    fbar = means + (sx2s * (I - means) / (sx2s + (means ** 2 / ENLs)))
    OIm[means != 0] = fbar[means != 0]
    return OIm
