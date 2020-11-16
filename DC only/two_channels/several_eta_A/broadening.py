#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Hao Ren <renh.cn@gmail.com>
#
# Distributed under terms of the LGPLv3 license.

#==============================================================================
# Module documentation
'''
FileName        : broadening.py
Purpose         : Perform Lorentz or Gaussian lineshape broadening for discrete data
Author          : Hao Ren
Version         : 0.2
Date            : May 31, 2017
usage           : python broadening -h
'''
#==============================================================================

from __future__ import print_function
import numpy as np
import argparse

class Convolution:
    '''
    Broadenging a given discrete data set using Lorentzian or Gaussian convolution
    '''
    def __init__(self, data, lb=None, hb=None, gamma=None, N=1000):
        self.data = data
        extension = (self.data[-1,0] - self.data[0,0] ) / 3.0

        if lb:
            self.lower_bound = lb
        else:
            self.lower_bound = self.data[0,0] - extension

        if hb:
            self.higher_bound = hb
        else:
            self.higher_bound = self.data[-1,0] + extension

        if gamma:
            self.gamma = gamma
        else:
            self.gamma = extension / 100. * 3

        self.NPoints = N
        self.X = np.linspace(self.lower_bound, self.higher_bound, self.NPoints)

    def Gaussian(self):
        Y = np.zeros(self.NPoints)
        for x0, y0 in self.data:
            Y += 1.0 / np.pi / self.gamma * np.exp(-(self.X - x0)**2 / self.gamma ** 2) * y0
        return Y

    def Lorentzian(self):
        Y = np.zeros(self.NPoints)
        for x0, y0 in self.data:
            Y += self.gamma / 2. / np.pi / ((self.X - x0)**2 + 0.25 * self.gamma ** 2) * y0
        return Y


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inp', help='Input filename with columnwise data', default=None)
    parser.add_argument('-o', '--out', help='Output file name', default='output.dat')

    parser.add_argument('-x', '--xcol', help='column of independent variables',
                        default=1, type=int)
    parser.add_argument('-y', '--ycol', help='column of dependent variables',
                        default=2, type=int)

    parser.add_argument('-g', '--gamma', help='Convolution parameter',
                        type=float, default=None)

    parser.add_argument('-L', '--low', help='Lower bound for independent variables',
                        type=float, default=None)
    parser.add_argument('-H', '--high', help='Higher bound for independent variables',
                        type=float, default=None)

    parser.add_argument('-m', '--method', help='Convolution method, G: Gaussian; L: Lorentzian; A: all/both')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-N', '--npoints', help='Number of points will be generated',
                        type=int, default=None)
    group.add_argument('-d', '--dist', help='Distance between points (independent)',
                       type=float, default=None)
    args = parser.parse_args()

    inp_fnm = args.inp
    out_fnm = args.out

    if inp_fnm:
        try:
            inp_data = np.loadtxt(inp_fnm)
        except:
            raise IOError('Can not load file {}.'.format(inp_fnm))
    else:
        raise ValueError('No data file specified. Use "-i" to specify the input data file.')

    if args.xcol > len(inp_data[0]) + 1 or args.ycol > len(inp_data[0]) + 1:
        raise ValueError(f'Column number greater than number of data columns {len(inp_data[0])}')
    inp_data = inp_data[:,(args.xcol-1, args.ycol-1)]

    idx = inp_data[:,0].argsort()
    inp_data = inp_data[idx]

    input_x_range = inp_data[-1,0] - inp_data[0,0]
    if args.gamma:
        if args.gamma < 0:
            raise ValueError('Unsurported negative Gamma')
        gamma = args.gamma
    else:
        if input_x_range > 0:
            gamma = input_x_range / 10.
        else:
            raise ValueError('Can not generate default Gamma value')

    if args.low is not None:
        lower_bound = args.low
    else:
        lower_bound = inp_data[0,0] - input_x_range / 3.0
    if args.high is not None:
        higher_bound = args.high
    else:
        higher_bound = inp_data[-1,0] + input_x_range / 3.0

    if args.dist:
        if args.dist == 0:
            raise ValueError('Zero distance between points not accepted.')
        npoints = (higher_bound - lower_bound) / args.dist + 1
    elif args.npoints:
        npoints = args.npoints
    else:
        npoints = 1000 # default number of points

    broadening = Convolution(inp_data, lb=lower_bound, hb=higher_bound, gamma=gamma, N=npoints)

    if args.method:
        method = args.method.upper()
        if method not in ['A', 'G', 'L']:
            raise ValueError('Not supported method. -h for details')
    else:
        method = 'A'


    with open(out_fnm, 'w') as out_fh:
        out_fh.write('# Convoluted data using {}\n'.format(sys.argv[0]))
        out_fh.write('# input data:           {}\n'.format(inp_fnm))
        out_fh.write('# Gamma:                {:.4G}\n'.format(gamma))
        out_fh.write('# Data range:           {:.4G} -- {:.4G}\n'.format(lower_bound, higher_bound))
        out_fh.write('# number of points:     {}\n'.format(npoints))
        out_fh.write('#'+'='*78 + '\n')
        out_fh.write('# {:^16}'.format('X'))
        if method == 'A':
            out_data = np.zeros([npoints, 3])
            out_fh.write('{:^18}'.format('Gaussian') + '{:^18}'.format('Lorentzian') + '\n')
            fmt = '{:18.6G}{:18.6G}{:18.6G}\n'
            out_data[:,0] = broadening.X
            out_data[:,1] = broadening.Gaussian()
            out_data[:,2] = broadening.Lorentzian()
        else:
            out_data = np.zeros([npoints, 2])
            fmt='{:18.6G}{:18.6G}\n'
            out_data[:,0] = broadening.X
            if method == 'G':
                out_fh.write('{:^18}\n'.format('Gaussian'))
                out_data[:,1] = broadening.Gaussian()
            elif method == 'L':
                out_fh.write('{:^18}\n'.format('Lorentzian'))
                out_data[:,1] = broadening.Lorentzian()
        out_fh.write('#'+'-'*78+'\n')
        for point in out_data:
            out_fh.write(fmt.format(*point))




