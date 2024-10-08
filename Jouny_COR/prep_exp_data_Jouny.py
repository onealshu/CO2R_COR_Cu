#!/usr/bin/env python

import sys, os
import numpy as np
from scipy.optimize import curve_fit, leastsq
from copy import deepcopy
sys.path.append('../.')
from plot_paper_data import _write_pickle_file

def _read_header(txtfile):
    with open(txtfile, 'r') as infile:
        hline = infile.readlines()[0][1:]
    return(hline)

def _read_meta_data(mfile):
    with open(mfile, 'r') as infile:
        lines = infile.readlines()
    dat = {}
    for l in lines:
        e = [s.strip() for s in l.split('=')]
        dat.update({e[0]:e[1]})
    return(dat)

if __name__ == "__main__":
    # read main data
    # no std std deviation
    full_data = {}
    for i in range(1,6):
        nfile = 'raw_data_%i.txt'%i
        keys = _read_header(nfile).split()
        val = np.loadtxt(nfile)
        val[:,2:] /= 100. # correct for percentage

        # prep data
        data = {keys[i]:np.zeros((val.shape[0], 2)) for i in range(len(keys))}
        for k in data:
            data[k][:,0] = val[:,keys.index(k)]
        
        mfile = 'meta_data_%i.txt'%i
        mdat = _read_meta_data(mfile)
        data.update(mdat)

        # sort into one file 
        full_data.update({mdat['catalyst']+'+pH'+str(mdat['pH']):data})
    

    # save data
    name = os.getcwd().split('/')[-1]
    _write_pickle_file("%s.pkl"%name, full_data)


