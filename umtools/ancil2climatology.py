#!/usr/bin/env python
"""
Copyright 2017 

author:  <scott.wales@unimelb.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import print_function
import mule
import argparse
import numpy


def no_validate(*args, **kwargs):
    pass


class OverrideOp(mule.DataOperator):
    def __init__(self):
        pass

    def new_field(self, source_fields):
        return source_fields[0].copy()

    def transform(self, source_fields, result_field):
        return source_fields[1].get_data()


def main():
    parser = argparse.ArgumentParser(
        description="Convert a time-series ancil file to a climatology by slicing to a selected year"
    )
    parser.add_argument("--year", type=int, help="Year to select")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()

    ff = mule.ancil.AncilFile.from_file(args.input)
    ff_out = ff.copy()

    clim_fields = {}

    override = OverrideOp()

    for field in ff.fields:
        if field.lbyr == args.year:
            clim_fields[field.lblev * 100 + field.lbmon] = field

    for field in ff.fields:
        if field.lbyr == args.year:
            ff_out.fields.append(field)
        else:
            ff_out.fields.append(
                override([field, clim_fields[field.lblev * 100 + field.lbmon]])
            )

    ff_out.validate = no_validate
    ff_out.to_file(args.output)


if __name__ == "__main__":
    main()
