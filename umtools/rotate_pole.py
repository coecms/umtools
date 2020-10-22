#!/g/data/hh5/public/apps/nci_scripts/python-analysis3
# Copyright 2020 Scott Wales
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

"""
Rotate the pole of a UM file
"""

import mule


class RotatePoleOp(mule.DataOperator):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def new_field(self, source_field):
        field = source_field.copy()
        if self.lat is not None:
            field.bplat = self.lat
        if self.lon is not None:
            field.bplon = self.lon
        return field

    def transform(self, source_field, new_field):
        return source_field.get_data()


def rotate_pole(mf: mule.UMFile, lat: float = None, lon: float = None):
    """
    Rotate the pole of a UM file

    Args:
        mf: Input UM file
        lat (float): Pole latitude
        lon (float): Pole longitude

    Returns:
        A copy of 'mf' with the pole rotated
    """

    out = mf.copy()

    if lat is not None:
        out.real_constants.north_pole_lat = lat

    if lon is not None:
        out.real_constants.north_pole_lon = lon

    op = RotatePoleOp(lat, lon)

    for f in mf.fields:
        out.fields.append(op(f))

    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input UM file", type=argparse.FileType("r"))
    parser.add_argument("--output", help="Output UM file", required=True)
    parser.add_argument("--lat", help="New pole latitude", type=float)
    parser.add_argument("--lon", help="New pole longitude", type=float)

    args = parser.parse_args()

    mf = mule.load_umfile(args.input)
    out = rotate_pole(mf, args.lat, args.lon)
    out.to_file(args.output)
