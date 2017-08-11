#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Jun 09, 2017 Fri
# Last update : 
#
# Imports
import numpy as np
import scipy as sp
import scipy.interpolate
import time

def interpolate_flux(infile, outfile,lambda1,lambda2):
    """ Interpolate the sed file in step of 1 Angstrom. """
    wave, flux6, flux12 = np.loadtxt(infile, skiprows=15, unpack=True,
                                   dtype='float', usecols=(0, 6, 12))
    #print('{} {} {}'.format('wave[0] = ', wave[0], ''))
    #print('{} {} {}'.format('flux[0] = ', flux[0], '\n'))

    # wavelength range to interpolate
    nums = int(lambda2 - lambda1) + 1
    waverange = np.linspace(lambda1, lambda2, num=nums, endpoint=True)
    #print('{} {} {}'.format('waverange :\n', waverange, ''))


    # interpolation
    #print('{} {} {}'.format('\nInterpolating flux from the file : ', infile, ' \n...'))
    iflux6 = sp.interpolate.interp1d(wave, flux6, kind='cubic')(waverange)
    iflux12 = sp.interpolate.interp1d(wave, flux12, kind='cubic')(waverange)


    # write to a file
    hdr = '%-14s %-14s %+18s'%('Wavelength', 'Flux6', 'Flux12')
    np.savetxt(outfile, list(map(list, zip(*[waverange, iflux6, iflux12]))),
               fmt=['%-13d','%.13e','%.13e'], delimiter='\t', newline='\n',
               header=hdr)


    # output info
    print('Interpolating from %d to %d from file: %s' % (lambda1,lambda2,infile) )
    print('Writing interpolated file to:', outfile, '\n')
    #print('{} {} {}'.format('\ninterpolation range :',  waverange, '\n'))
    #print('{} {} {}'.format('input file            : ', infile, ''))
    #print('{} {} {}'.format('output file           :',  outfile, ''))
    
def main():
    lambda1 = 1000
    lambda2 = 12000
    # read data from the file
    infileb  = 'sed/ssp_pf.cat'
    outfileb = 'sed/ssp_pf_interpolated.csv'
    infiled  = 'sed/exp9_pf.cat'
    outfiled = 'sed/exp9_pf_interpolated.csv'
    interpolate_flux(infileb, outfileb,lambda1,lambda2)
    interpolate_flux(infiled, outfiled,lambda1,lambda2)
    
    
##==============================================================================
## Main program
##==============================================================================
if __name__ == '__main__':

    # beginning time
    begin_time,begin_ctime = time.time(), time.ctime()

    # run main program
    main()

    # print the time taken
    end_time,end_ctime  = time.time(), time.ctime()
    seconds             = end_time - begin_time
    m, s                = divmod(seconds, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print('\nBegin time: ', begin_ctime,'\nEnd   time: ', end_ctime,'\n' )
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))

