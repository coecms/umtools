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

def main():
    parser = argparse.ArgumentParser(description="Convert a file to netcdf using Iris")
    parser.add_argument('--output','-o', help="Output file name")
    parser.add_argument('input', help="Input file name")
    args = parser.parse_args()

    if args.output:
        outfile = args.output
    else:
        basename = os.path.basename(args.input)
        (root, ext) = os.path.splitext(basename)
        outfile = root + '.nc'

    try:
        convert(infile, outfile)
        print("Created %s"%outfile)
    except Exception:
        print("Unable to convert %s to NetCDF format"%args.input)

def convert(infile, outfile):
    cubes = iris.load(infile)
    iris.fileformats.netcdf.save(cubes, outfile)

if __name__ == '__main__':
    main()

