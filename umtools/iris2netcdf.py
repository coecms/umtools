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
import tqdm
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Convert a file to netcdf using Iris. Multiple inputs will be merged into a single file")
    parser.add_argument('--output','-o', help="Output file name")
    parser.add_argument('--compression','-C',help="Compression level",choices=range(0,10),default=4,metavar='{0-9}',type=int)
    parser.add_argument('input', help="Input file name [UM/GRIB/NetCDF format]", nargs="+")
    args = parser.parse_args()

    if args.output:
        outfile = args.output
    else:
        basename = os.path.basename(args.input[0])
        (root, ext) = os.path.splitext(basename)
        outfile = root + '.nc'

    try:
        cubes = iris.load(args.input)

        save_netcdf(cubes, outfile, compression=args.compression)
        print("Created %s"%outfile)
    except Exception:
        print("Unable to convert %s to NetCDF format"%args.input)
        raise

def save_netcdf(cubes, path, compression=4):
    """
    Save Iris cubes to netcdf, with chunking and compression
    """

    with iris.fileformats.netcdf.Saver(path, 'NETCDF4') as saver:
        for c in tqdm.tqdm(cubes):
            # Make sure time is a real dimension
            if len(c.coords('time', dim_coords=False)) != 0:
                c = iris.util.new_axis(c, 'time')

            if c.has_lazy_data():
                da = c.core_data()
                chunks = [c if c < 1000 else 1000 for c in da.chunksize]
            else:
                chunks = da.shape

            saver.write(c, unlimited_dimensions='time',
                    chunksizes=chunks, zlib=True, complevel=compression, shuffle=True)

if __name__ == '__main__':
    main()

