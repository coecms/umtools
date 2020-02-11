#!/g/data/hh5/public/apps/miniconda3/envs/analysis3-20.01/bin/python
"""
Extract a year of data from a UM ancil file, and use it to create a new periodic ancillary

    ./extract_ancil_year.py --year=2000 --output=SPARCO3_2000.anc ~access/data/ancil/CMIP5/SPARCO3_1850-2009_L38.anc
"""

import mule
import argparse

def main():
    parser = argparse.ArgumentParser(description="Extract a year from an ancillary file as a periodic ancil")
    parser.add_argument('input', type=argparse.FileType('rb'), help="Input ancil file")
    parser.add_argument('--year', type=int, help="Year to extract", required=True)
    parser.add_argument('--output', type=argparse.FileType('wb'), help="Output ancil file", required=True)

    args = parser.parse_args()

    infile = mule.ancil.AncilFile.from_file(args.input)
    outfile = infile.copy()
    outfile.fixed_length_header.time_type = 2 # Periodic

    for f in infile.fields:
        # Select fields where the year matches the target year
        if f.lbyr == args.year:
            outfile.fields.append(f)

    outfile.level_dependent_constants = None
    outfile.to_file(args.output)

if __name__ == '__main__':
    main()
