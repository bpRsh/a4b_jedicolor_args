#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel, Physics PhD Student, Ohio University
# Date        : Jul 06, 2017 Thu
# Last update :
# Imports
import numpy as np
import pandas as pd
import time

def main():
    """Main Module."""
    infile = 'jedicolor_args.txt'
    colnames = ['c0', 'c1']
    df = pd.read_csv(infile,sep=r'\s+', header = None,skiprows = 0,
                     comment='#',names=colnames,usecols=(0,1))


    a = sum(df.c0) + sum(df.c1)
    print(a)
    print('Difference from 1 = ', abs(1-a))
    

if __name__ == '__main__':
    main()

