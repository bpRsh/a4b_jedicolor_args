#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Jun 09, 2017 Fri
# Last update : 
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



def wavelengths(z_g, z_cutout):
    """Here 22 numbers has 21 integral ranges.
    
    """
    # Wavelength for lsst r band and hst f814 filter
    laml0  = 5520 / (1 + z_g)  # 2208.0                       
    laml20 = 6910 / (1 + z_g)  # 2764.0
    lamh0  = ( 8333 - (2511/2) ) / (1 + z_cutout) # 7077.5 / 1.2 = 5897.9 
    lamh20 = ( 8333 + (2511/2) ) / (1 + z_cutout) # 9588.5 / 1.2 = 7990.4

    # Make wavelentghs integer
    # I have interpolated sed wavelenths to nearest Angstroms.
    laml0  = round(laml0)  # 2208                       
    laml20 = round(laml20) # 2764
    lamh0  = round(lamh0)  # 5898 
    lamh20 = round(lamh20) # 7990

    # List of 22 values for 21 intervals.
    laml   = np.linspace(start=laml0,stop=laml20,num=22,endpoint=True)
    lamh   = np.linspace(start=lamh0,stop=lamh20,num=22,endpoint=True)
    
    # Make integers
    laml   = [round(i) for i in laml]
    lamh   = [round(i) for i in lamh]
    
    # Return Value
    return [laml, lamh]

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
    integral= simps(flx)
    
    # Return Values
    return integral



def write_jedicolor_args():
    """Calculation of arguments for jedicolor.
    
.. math:: b[0] = (Ilb/Ilbt) * (Nb / N
.. math:: Nb   = Ilbt/Ihbt
.. math:: b[0] = \int_{\lambda0}^{\lambda1} f_b d\lambda
    
    
.. math:: Ilb = \int_{\lambda0}^{\lambda1} f_b(\lambda)d\lambda

.. math:: Ihb = \int_{\lambda_{hst0}}^{\lambda{hst1}} f_b(\lambda)d\lambda

.. math:: Ilbt = \int_{\lambda0}^{\lambda_{20}} f_b(\lambda)d\lambda

.. math:: Ihbt = \int_{\lambda_{hst0}}^{\lambda_{hst20}} f_b(\lambda)d\lambda

.. math:: N_b = \\frac{Ilbt}{Ihbt}

.. math:: N_d = \\frac{Ilht}{Ihht}


.. math:: b[0] = \\frac{Ilb}{Ilbt} \\quad \\frac{Ilbt/Ihbt}{N_b + N_d}

.. math:: b[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_b(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_b(\\lambda)d\\lambda} \\quad \\frac{(\\int_{\\lambda0}^{\\lambda_{20}} f_b(\\lambda)d\\lambda)/(\\int_{\\lambda_{hst0}}^{\\lambda_{hst20}} f_b(\\lambda)d\\lambda)}{N_b + N_d}


      
    
    """

    # Wavelenths
    laml, lamh = wavelengths(z_g, z_cutout)
    print('laml = \n', laml )
    print('lamh = \n', lamh )
    
    
    Ilb  = integrate_flux(infileb, 'flux6', laml[0], laml[0+1]) 

    # LSST r band 6 Gyr old integrals for bulge and disk (LSST has narrowbands)
    Ilb  = [integrate_flux(infileb, 'flux6', laml[i], laml[i+1]) for i in range(21) ]
    Ild  = [integrate_flux(infiled, 'flux6', laml[i], laml[i+1]) for i in range(21) ]
    
    # LSST r band 6 Gyr old total range integrals for bulge and disk
    Ilbt =   integrate_flux(infileb, 'flux6', laml[0], laml[21])
    Ildt =   integrate_flux(infiled, 'flux6', laml[0], laml[21])

    # HST f814 filter 12 Gyr old total integrals for bulge and disk
    Ihbt =   integrate_flux(infileb, 'flux12', lamh[0], lamh[21])
    Ihdt =   integrate_flux(infiled, 'flux12', lamh[0], lamh[21])

    # Normalization has all hst, lsst, bulge, and disk parts
    Nb = Ilbt/Ihbt
    Nd = Ildt/Ihdt
    Fb = 1.0 / Ihbt / (Nb + Nd)
    Fd = 1.0 / Ihdt / (Nb + Nd)
    b  = [i*Fb for i in Ilb]
    d  = [i*Fd for i in Ild]
    
    # Write jedicolor_args.csv
    print('\nWriting: %s\n'%(outfile))
    #np.savetxt(outfile, np.array([b,d]).T, fmt=['%.14e', '%.14e'], delimiter='\t')
    np.savetxt(outfile, np.array([b,d]).T, fmt=['%.5f', '%.5f'], delimiter='\t')


##==============================================================================
## Main program
##==============================================================================
if __name__ == '__main__':
    # beginning time
    begin_time,begin_ctime = time.time(), time.ctime()

    # run main program
    write_jedicolor_args()

    # print the time taken
    end_time,end_ctime  = time.time(), time.ctime()
    seconds             = end_time - begin_time
    m, s                = divmod(seconds, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print('\nBegin time: ', begin_ctime,'\nEnd   time: ', end_ctime,'\n' )
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))

