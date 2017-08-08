#!/usr/bin/env python
# Copyright 2017 ARC Centre of Excellence for Climate Systems Science
# author: Scott Wales <scott.wales@unimelb.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function

import iris
iris.FUTURE.netcdf_no_unlimited = True
import subprocess
import tempfile
import argparse
import os

var_names = {
    301 : 'qflux',
    302 : 'mask',
    303 : 'heat',
    304 : 'taux',
    305 : 'sst',
    306 : 'pat'
}

long_names = {
    301 : 'flux correction',
    302 : 'sea mask',
    303 : 'flux climatology',
    304 : 'zonal wind climatology',
    305 : 'sea surface temperature',
    306 : 'recharge oscillator pattern'
}


def main():
    parser = argparse.ArgumentParser(description="Convert a slab ocean ancillary file to either netcdf or um format")
    parser.add_argument('command', choices = ['to_netcdf', 'to_um'])
    parser.add_argument('--output','-o', help="Output file name")
    parser.add_argument('input', help="Input file name")
    args = parser.parse_args()

    if args.command == 'to_netcdf':
        if args.output:
            outfile = args.output
        else:
            basename = os.path.basename(args.input)
            (root, ext) = os.path.splitext(basename)
            outfile = root + '.nc'

        try:
            to_netcdf(args.input, outfile)
            print("Created %s"%outfile)
        except Exception:
            print("Unable to convert %s to NetCDF format"%args.input)

    else:
        if args.output:
            outfile = args.output
        else:
            basename = os.path.basename(args.input)
            (root, ext) = os.path.splitext(basename)
            outfile = root + '.ancil'

        try:
            to_um(args.input, outfile)
        except Exception as e:
            print("Unable to convert %s to UM format"%args.input)
#            raise e

def to_netcdf(infile, outfile):
    cubes = iris.load(infile)
    for cube in cubes:
        secitem = cube.attributes['STASH'].section * 1000 + cube.attributes['STASH'].item
        cube.var_name = var_names[secitem]
        cube.long_name = long_names[secitem]
    iris.fileformats.netcdf.save(cubes, outfile)

def to_um(infile, outfile):
    with tempfile.TemporaryFile(mode='w+') as namelist:

        content = """
 &nam_config
  ICAL = 2,
  ISIZE = 64,
  L32BIT = .FALSE.,
  VERSION = 6.6,
  LBIGENDOUT = .TRUE.,
  LWFIO = .FALSE.,
  NNCFILES = 1
  NCFILES = "%(infile)s"
 /

 &nam_gridconfig
  IAVERT = 0,
  IOVERT = 0,
  LDEEPSOIL = .FALSE.
 /

 &nam_ozone
 /

 &nam_smow
 /

 &nam_slt
 /

 &nam_soil
 /

 &nam_veg
 /

 &nam_vegfrac
 /

 &nam_vegfunc
 /

 &nam_vegdist
 /

 &nam_sst
 /

 &nam_ice
 /

 &nam_orog
 /

 &nam_mask
 /

 &nam_lfrac
 /

 &nam_ausrmulti
 /

 &nam_ausrancil
  LAUSRANCIL = .TRUE.,
  AUSRANCIL_FILEOUT = "%(outfile)s",
  LAUSRANCIL_PERIODIC = .TRUE.,
  IAUSRANCIL_TIMEUSAGE1 = 0,
  IAUSRANCIL_TIMEUSAGE2 = 0,
  IAUSRANCIL_STARTDATE(1) = 0000,
  IAUSRANCIL_STARTDATE(2) = 1,
  IAUSRANCIL_STARTDATE(3) = 16,
  IAUSRANCIL_STARTDATE(4) = 0,
  IAUSRANCIL_STARTDATE(5) = 0,
  IAUSRANCIL_STARTDATE(6) = 0,
  IAUSRANCIL_NTIMES = 12,
  IAUSRANCIL_INTERVAL = 1,
  IAUSRANCIL_INTUNIT = 1,
  LAUSRANCIL_MM = .TRUE.
  IAUSRANCIL_NFIELD = 6
  IAUSRANCIL_FILEINID(1) = 1,
  IAUSRANCIL_STASHCODE(1) = 301,
  IAUSRANCIL_PPCODE(1) = 0,
  AUSRANCIL_NCNAME(1) = "%(var_name301)s",
  IAUSRANCIL_DATATYPE(1) = 1,
  IAUSRANCIL_MASKTYPE(1) = 0,
  IAUSRANCIL_MASK(1) = 0,
  IAUSRANCIL_FILEINID(2) = 1,
  IAUSRANCIL_STASHCODE(2) = 302,
  IAUSRANCIL_PPCODE(2) = 0,
  AUSRANCIL_NCNAME(2) = "%(var_name302)s",
  IAUSRANCIL_DATATYPE(2) = 1,
  IAUSRANCIL_MASKTYPE(2) = 0,
  IAUSRANCIL_MASK(2) = 0,
  IAUSRANCIL_FILEINID(3) = 1,
  IAUSRANCIL_STASHCODE(3) = 303,
  IAUSRANCIL_PPCODE(3) = 0,
  AUSRANCIL_NCNAME(3) = "%(var_name303)s",
  IAUSRANCIL_DATATYPE(3) = 1,
  IAUSRANCIL_MASKTYPE(3) = 0,
  IAUSRANCIL_MASK(3) = 0,
  IAUSRANCIL_FILEINID(4) = 1,
  IAUSRANCIL_STASHCODE(4) = 304,
  IAUSRANCIL_PPCODE(4) = 0,
  AUSRANCIL_NCNAME(4) = "%(var_name304)s",
  IAUSRANCIL_DATATYPE(4) = 1,
  IAUSRANCIL_MASKTYPE(4) = 0,
  IAUSRANCIL_MASK(4) = 0,
  IAUSRANCIL_FILEINID(5) = 1,
  IAUSRANCIL_STASHCODE(5) = 305,
  IAUSRANCIL_PPCODE(5) = 0,
  AUSRANCIL_NCNAME(5) = "%(var_name305)s",
  IAUSRANCIL_DATATYPE(5) = 1,
  IAUSRANCIL_MASKTYPE(5) = 0,
  IAUSRANCIL_MASK(5) = 0,
  IAUSRANCIL_FILEINID(6) = 1,
  IAUSRANCIL_STASHCODE(6) = 306,
  IAUSRANCIL_PPCODE(6) = 0,
  AUSRANCIL_NCNAME(6) = "%(var_name306)s",
  IAUSRANCIL_DATATYPE(6) = 1,
  IAUSRANCIL_MASKTYPE(6) = 0,
  IAUSRANCIL_MASK(6) = 0,
 /

 &nam_ts1
 /

 &nam_flux
 /

 &nam_ousrmulti
 /

 &nam_ousrancil
 /

 &nam_genanc_config
  NANCFILES = 1
 /

 &nam_genanc
  LGENANC_FILE(1) = .FALSE.,

 /

        """%{'infile': infile, 'outfile': outfile,
             'var_name301' : var_names[301],
             'var_name302' : var_names[302],
             'var_name303' : var_names[303],
             'var_name304' : var_names[304],
             'var_name305' : var_names[305],
             'var_name306' : var_names[306]
             }

        namelist.write(content)
        namelist.flush()
        namelist.seek(0)

        with subprocess.Popen(['/projects/access/bin/mkancil0.57'], stdin=namelist, stdout=subprocess.PIPE) as proc:
            print(proc.stdout.read().decode('ascii'))

if __name__ == '__main__':
    main()
