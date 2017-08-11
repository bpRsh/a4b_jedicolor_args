#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel, Physics PhD Student, Ohio University
# Date        : Jul 06, 2017 Thu
# Last update :


def main():
    """Main Module."""
    # Imports
    import numpy as np
    import pandas as pd
    import time

    laml = np.linspace(2208,2764,num=22)
    laml = [round(i) for i in laml]
    print('laml = ', laml)

    for i in range(len(laml) -1):
        x = laml[i]
        y = laml[i+1]
        print('x,y = ', x, y)
    

if __name__ == '__main__':
    main()


