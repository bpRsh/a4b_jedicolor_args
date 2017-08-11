#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel, Physics PhD Student, Ohio University
# Date        : Jul 17, 2017 Mon
# Last update : Jul 17, 2017 Mon
#
# Imports
import time
import numpy as np
import scipy as sp
import pandas as pd
from scipy.integrate import simps

# Input parameters
z_g      = 1.5
z_cutout = 0.2

# General jedimaster
infileb  = "sed/ssp_pf_interpolated.csv"
infiled  = "sed/exp9_pf_interpolated.csv"
outfile  = 'jedicolor_args.txt'

def integrate_flux(infile, colname, wav_start, wav_end):
    """Integrate the flux between two points of input sed file.
    
    .. note::
    
       Sometimes pd.read_csv fails, so use np.genfromtxt to read the datafile.
       
       In np.genfromtxt dtype is determined indivisually.
       
       https://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html
    
    """    
    
    wav,flux6,flux12 = np.genfromtxt(infileb,usecols=(0,1,2),unpack=True)
    
    if colname=='flux6':
        flx = [flux6[i] for i in range(len(wav)) if (wav[i] >= wav_start and wav[i] <= wav_end) ]
        
    else:
        flx = [flux12[i] for i in range(len(wav)) if (wav[i] >= wav_start and wav[i] <= wav_end) ]
    
    
    # Debug
    #print(flx)
    
    # Calcualte
    integral= simps(flx)
    
    # Return Values
    return integral

def integrate_flux2(infile, colname, wav_start, wav_end):
    """Integrate the flux between two points of input sed file.
    
    .. note::
    
       Sometimes pd.read_csv fails, so use np.genfromtxt to read the datafile.
    
    """  
    wav,flux6,flux12 = np.genfromtxt(infileb,delimiter=None,dtype=float,unpack=True)  
    columns = ['wav','flux6','flux12']
    df      = pd.DataFrame(np.transpose([wav,flux6,flux12]),columns=columns)
    df2     = df[(df['wav']>=wav_start) & (df['wav']<=wav_end)]
    flx     = df2[colname]
    integral= simps(flx)
    
    print(df2)
    
    # Return Values
    return integral


def integrate_flux3(infile, colname, wav_start, wav_end):
    """Integrate the flux between two points of input sed file.
    
    
    
    
    .. note::
    
       Sometimes pd.read_csv fails, so use np.genfromtxt to read the datafile.
    
    """    
    columns = ['wav','flux6','flux12']
    df      = pd.read_csv(infile, sep=r'\s+',names=columns)
    
    
    print(df.head())
    #df2     = df[(df['wav']>=wav_start) & (df['wav']<=wav_end)]
    #flx     = df2[colname]
    #integral= simps(flx)
    
    # Return Values
    #return integral
    

if __name__ == '__main__':
    integrate_flux2(infileb, 'flux6', 1002, 1008)
