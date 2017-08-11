#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel, Physics PhD Student, Ohio University
# Date        : Jul 17, 2017 Mon
#
# Imports
import numpy as np
import pandas as pd
import time

def create_flat_sed(outfile):
    """ Create flat sed file with three columns """ 
    with open (outfile,'w') as fo:
        x = 0
        for i,x in enumerate(list(range(1000, 12000+1))):
            print(x, '    {:.5f}'.format(0.00001* i)*2 ,file=fo)

if __name__ == '__main__':
    create_flat_sed('sed/flat_sed.txt')
    create_flat_sed('tmp.txt')
